from dokanki.converter import converter
from dokanki.logger import logger
import tempfile
import re


class PDSConverter(converter.Converter):

    def __init__(self):
        self.logger = logger(__name__)

    def supports(self, uri):
        return uri.endswith('.pds')

    def _extract_correct_answers(self, question):
        question = re.sub('\[#\d] ', '', question)
        question = re.sub('\*\d\*', '', question).strip('*').strip(' ')
        title = question.split('\n')[0]
        all_answers = question.split('\n', 1)
        if len(all_answers) == 1:
            return title, []
        all_answers = all_answers[1].replace('\n>', '\n>>').split('\n>')
        correct_answers = []
        for answer in all_answers:
            if answer.startswith('>'):
                answer = re.sub('\S\)', '', answer.strip('>')).strip(' ')
                correct_answers.append(answer)
        return title, correct_answers

    def _convert(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        content = content.split('\n\n')
        result = []
        for question in content:
            if question.startswith('<options>'):
                continue
            title, answers = self._extract_correct_answers(question)
            if not answers:
                continue
            title = '<h1>{}</h1>\n'.format(title)
            answers = [x + '\n' for x in answers]
            result.append((title, answers))
        return result

    def _write_to_file(self, file_path, converted_questions):
        # with open(file_path, 'w') as f:
        f = open(file_path, 'w')
        for question in converted_questions:
            f.write(question[0])
            f.write('<p>\n')
            for answer in question[1]:
                f.write(answer)
                f.write('<hr>\n')
            f.write('</p>\n')

    def convert(self, temp_dir, url):
        file = tempfile.mktemp(prefix='dokanki', suffix='.html', dir=temp_dir)
        self.logger.info("Converting {} to {}".format(url, file))
        self._write_to_file('{}/dokanki.html'.format(temp_dir), self._convert(url))
        return file
