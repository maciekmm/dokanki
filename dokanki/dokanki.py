import json
import os
import zipfile
from functools import reduce

import genanki as genanki

from dokanki.converter.gdocs import GDocsConverter
from dokanki.extractor.html import HTMLExtractor


class UnsupportedFormatError(object):
    pass


class Dokanki(object):
    extractors = [
        HTMLExtractor
    ]
    converters = [
        GDocsConverter()
    ]
    sources = []
    cards = []

    def __init__(self, name, id, steps=[10, 20, 30]):
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
                return extractor(level).extract(uri)

        for converter in self.converters:
            if converter.supports(uri):
                return self._extract(converter.convert(uri))

        raise UnsupportedFormatError()

    def write(self, file_name):
        images = []
        deck = genanki.Deck(self.id, self.name)

        for card in self.cards:
            if card.media is not None:
                for img in card.media:
                    images.append(img)

            sort_tag = reduce(lambda acc, x: acc + x + '/', card.hierarchy, '') + card.title
            deck.add_note(
                genanki.Note(guid=genanki.guid_for(card.title), model=self._note_model,
                             fields=[card.title, card.content, sort_tag]))

        package = genanki.Package(deck)
        package.media_files = images
        temporary_file = file_name + '.dokanki.temp'
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
        os.remove(temporary_file)
