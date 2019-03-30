import copy
import os
import re
from functools import reduce

from bs4 import BeautifulSoup

from dokanki.extractor import extractor
from dokanki.extractor.html.hierarchical import HierarchicalExtractor
from dokanki.extractor.html.ordered_list import OrderedListExtractor
from dokanki.flashcard import FlashCard
from dokanki.logger import logger


class HTMLExtractor(extractor.Extractor):
    extraction_methods = [
        OrderedListExtractor,
        HierarchicalExtractor
    ]

    @staticmethod
    def supports(uri: str):
        return uri.endswith(".html")

    def __init__(self, level=2, header_prefix="^(?:\\s*\\d+\\.\\s*)+(\[[^]]+])?\\s*"):
        self._header_prefix = re.compile(header_prefix)
        self.level = level
        self.logger = logger(__name__)

    def extract(self, uri):
        with open(uri) as fp:
            bs = BeautifulSoup(fp, features="html.parser")
            return max([self._extract_from_soup(os.path.dirname(os.path.realpath(uri)), method, bs) for method in
                        self.extraction_methods], key=lambda e: len(e))

    def _extract_from_soup(self, directory, method, bs: BeautifulSoup):
        top_level = method.extract_headers(bs, self.level)
        cards = []
        for i, header in enumerate(top_level):
            title = self._clean_header(header.text)
            if len(title) == 0:
                continue
            sort_tag = [self._clean_header(header) for header in method.find_ancestors(header, self.level)]
            sort_tag.append(title)
            images, content = self.extract_flat_content(header, top_level[i + 1] if len(top_level) > i + 1 else None)
            cards.append(FlashCard(title, content, map(lambda url: directory + '/' + url, images), sort_tag))
        return cards

    def _clean_header(self, text: str) -> str:
        matches = self._header_prefix.search(text)
        if matches is None:
            return text.strip(' ')
        return text.replace(matches.group(0), "").strip(' ')

    @staticmethod
    def extract_flat_content(element, end):
        content = []
        image_files = []
        while element.next_sibling is not None and element.next_sibling != end:
            element = element.next_sibling
            images = element.find_all(name="img")
            for image in images:
                # Return the complete image path for genanki to correctly include them in deck zip
                image_files.append(image['original_src'] if image.has_attr('original_src') else image['src'])
                # After inclusion the files end up in root directory and media file mapping does not seem to work
                image['original_src'] = image['src']
                image['src'] = image['src'].split('/')[-1]
            content.append(element.prettify())
        return image_files, reduce(lambda acc, val: acc + val, content, '')
