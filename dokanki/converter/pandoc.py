import pypandoc


class Pandoc:

    def convert(self, source, format, output):
        pypandoc.convert_file(source, format, outputfile=output)
