from bs4 import BeautifulSoup


class OrderedListExtractor:
    """
    GDocs style <ol> based element extractor
    """

    @staticmethod
    def find_ancestors(element, level):
        return [];

    @staticmethod
    def _get_list_id(list_element: BeautifulSoup):
        if not list_element.has_attr('class'):
            return None
        for clazz in list_element['class']:
            if clazz.startswith('lst'):
                return clazz
        return None

    @staticmethod
    def extract_headers(document: BeautifulSoup, level):
        return max(map(lambda lid: document.find_all(class_=lid),
                       set(filter(lambda x: x is not None,
                                  map(OrderedListExtractor._get_list_id, document.find_all(name="ol"))))),
                   key=lambda els: len(els))
