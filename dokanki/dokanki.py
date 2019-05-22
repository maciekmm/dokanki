import json
import os
import shutil
import tempfile
import zipfile
from functools import reduce

import genanki as genanki

from dokanki.converter.gdocs import GDocsConverter
from dokanki.extractor.pds import PDSExtractor
from dokanki.converter.pandoc import Pandoc
from dokanki.extractor.html.html import HTMLExtractor
from dokanki.logger import logger as log


class UnsupportedFormatError(Exception):
    pass


class Dokanki(object):
    extractors = [
        HTMLExtractor,
        PDSExtractor
    ]
    converters = [
        GDocsConverter(),
        Pandoc()
    ]
    sources = []
    cards = []
    temp_dirs = []

    def __init__(self, name, id, steps=[10, 20, 30], logger=log(__name__)):
        self.name = name
        self.id = id if id is not None else genanki.guid_for(id)
        self.steps = steps
        self._note_model = genanki.Model(
            self.id,
            'Model ' + self.name,
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Hierarchy'}
            ],
            templates=[
                {
                    'name': self.name,
                    'qfmt': '<h1>{{Question}}</h1>',
                    'afmt': '{{FrontSide}}<hr><p>{{Hierarchy}}</p><hr id="answer">{{Answer}}',
                },
            ])
        self.logger = logger

    def add_source(self, url, level):
        self.sources.append((url, level))

    def extract(self):
        for source in self.sources:
            for card in self._extract(source):
                self.cards.append(card)
        return self

    def _extract(self, source):
        uri, level = source
        for extractor in self.extractors:
            if extractor.supports(uri):
                extracted = extractor(level).extract(uri)
                self.logger.info("Extracting {} cards using {}...".format(len(extracted), extractor.__name__))
                return extracted

        for converter in self.converters:
            if converter.supports(uri):
                self.logger.info(
                    "Using {} converter.".format(converter.__class__.__name__))
                temp_dir = tempfile.mkdtemp(prefix="dokanki")
                self.temp_dirs.append(temp_dir)
                return self._extract((converter.convert(temp_dir, uri), level))

        raise UnsupportedFormatError()

    def write(self, file_name):
        images = []
        deck = genanki.Deck(self.id, self.name)

        for card in self.cards:
            if card.media is not None:
                [images.append(img) for img in card.media]

            sort_tag = reduce(lambda acc, x: acc + x + '/', card.hierarchy, '')
            deck.add_note(
                genanki.Note(guid=genanki.guid_for(card.title), model=self._note_model,
                             fields=[card.title, card.content, sort_tag]))

        package = genanki.Package(deck)
        package.media_files = images
        temporary_file = file_name + '.dokanki.temp'
        self.logger.info("Assembling Anki database file {}.".format(file_name))
        package.write_to_file(temporary_file)

        # Workaround for genanki bug
        # Anki wants every image to be in root directory, this fixes paths
        for i in range(len(package.media_files)):
            package.media_files[i] = package.media_files[i].split('/')[-1]

        zin = zipfile.ZipFile(temporary_file, 'r')
        zout = zipfile.ZipFile(file_name, 'w')
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename != 'media':
                zout.writestr(item, buffer)

        media_json = dict(enumerate(package.media_files))
        zout.writestr('media', json.dumps(media_json))
        zout.close()
        zin.close()
        self.logger.info("Cleaning up temporary files.")
        os.remove(temporary_file)
        # for temp_dir in self.temp_dirs:
        #     shutil.rmtree(temp_dir)
