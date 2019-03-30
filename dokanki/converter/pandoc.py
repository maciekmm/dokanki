import pypandoc

from dokanki.converter import converter
import tempfile


class Pandoc(converter.Converter):

    def supports(self, uri):
        return not uri.startswith('http')

    def convert(self, working_dir, source):
        file = tempfile.mktemp(prefix='dokanki', suffix='.html', dir=working_dir)
        print("Converting {} to {}.".format(source, file))
        pypandoc.convert_file(source, to='html', outputfile=file)
        return file
