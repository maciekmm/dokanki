import os
import re
from functools import reduce

from bs4 import BeautifulSoup

from dokanki.extractor import extractor
from dokanki.flashcard import FlashCard


class HTMLExtractor(extractor.Extractor):

    @staticmethod
    def supports(uri: str):
        return uri.endswith(".html")

    def __init__(self, level=2, header_prefix="^(?:\\s*\\d+\\.)+\\s*(\[[^]]+])?\\s*"):
        self._header_prefix = re.compile(header_prefix)
        self.level = level

    def extract(self, uri):
        with open(uri) as fp:
            bs = BeautifulSoup(fp, features="html.parser")
            return self._extract_from_soup(os.path.dirname(os.path.realpath(uri)), bs)

    def _extract_from_soup(self, directory, bs: BeautifulSoup):
        top_level = bs.find_all("h{}".format(self.level))
        cards = []
        for header in top_level:
            title = self._clean_header(header.text)
            sort_tag = reduce(lambda acc, x: acc + x + '/', self._find_ancestors(header, self.level), '') + title
            images, content = self._extract_content(header)
            cards.append(FlashCard(title, content, map(lambda url: directory + '/' + url, images), sort_tag))
        return cards

    def _clean_header(self, text: str) -> str:
        matches = self._header_prefix.search(text)
        if matches is None:
            return text
        return text.replace(matches.group(0), "")

    def _find_ancestors(self, element, level):
        if level == 1 or element is None:
            return []
        ancestors = []

        while level > 1 and element is not None:
            level -= 1
            element = element.find_previous("h{}".format(level))
            ancestors.append(self._clean_header(element.text))

        ancestors.reverse()
        return ancestors

    def _extract_content(self, element):
        end = element.find_next(name=re.compile("h[1-{}]".format(self.level)));
        content = []
        image_files = []
        while element.next_sibling is not None and element.next_sibling != end:
            element = element.next_sibling
            images = element.find_all(name="img")
            for image in images:
                # Return the complete image path for genanki to correctly include them in deck zip
                image_files.append(image['src'])
                # After inclusion the files end up in root directory and media file mapping does not seem to work
                image['src'] = image['src'].split('/')[-1]
            content.append(element.prettify())
        return image_files, reduce(lambda acc, val: acc + val, content, '')
