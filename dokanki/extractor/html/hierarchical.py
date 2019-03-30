from bs4 import BeautifulSoup


class HierarchicalExtractor:
    """
    <h{}> based element extractor
    """

    @staticmethod
    def find_ancestors(element: BeautifulSoup, level):
        if level == 1 or element is None:
            return []
        ancestors = []

        while level > 1 and element is not None:
            level -= 1
            element = element.find_previous("h{}".format(level))
            if element is None:
                continue
            ancestors.append(element.text)
        ancestors.reverse()
        return ancestors

    pass

    @staticmethod
    def extract_headers(document: BeautifulSoup, level):
        return document.find_all("h{}".format(level))
