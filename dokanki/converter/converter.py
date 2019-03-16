class Converter:
    """"""
    def convert(self, url):
        pass

    def converts_to(self):
        """
        :return: target format of this converter
        """
        return ""

    def supports(self, url):
        """
        reports whether this converter supports converting given uri
        :param url:
        :return:
        """
        return False
