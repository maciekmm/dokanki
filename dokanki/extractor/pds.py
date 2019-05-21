from dokanki.extractor import extractor
from dokanki.flashcard import FlashCard

import re


class PDSExtractor(extractor.Extractor):

    @staticmethod
    def supports(uri: str):
        return uri.endswith('.pds')

    def __init__(self, level):
        self.level = level

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

    def extract(self, uri):
        with open(uri, 'r') as file:
            content = file.read()
        content = content.split('\n\n')
        cards = []
        for question in content:
            if question.startswith('<options>'):
                continue
            title, answers = self._extract_correct_answers(question)
            if not answers:
                continue
            answers = [x + '\n' for x in answers]

            cards.append(FlashCard(title, ''.join(answers), None, ''))
        return cards
