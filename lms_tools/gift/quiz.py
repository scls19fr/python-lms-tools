from ..base import Quiz, Question
from .formatter import DefaultGiftQuizFormatter, DefaultGiftQuestionFormatter
# from .distractor import DefaultDistractorKeyParser


class GiftDistractor():
    def __init__(self, text, value, feedback=""):
        self.text = text
        self.feedback = feedback
        self.value = value


class GiftQuestion(Question):
    def __init__(self, stem="", distractors=None, name=None, comment=""):
        self.stem = stem
        if name is None:
            name = stem
        self.name = name
        if distractors is None:
            distractors = []
        self.distractors = distractors
        self.comment = comment
        self._default_formatter = DefaultGiftQuestionFormatter()

    def append_distractor(self, distractor):
        assert isinstance(distractor, GiftDistractor)
        self.distractors.append(distractor)

    @property
    def sum_values(self):
        result = 0
        for distractor in self.iter_distractors():
            result += distractor.value
        return result

    def normalize_values(self):
        for distractor in self.iter_distractors():
            distractor.value = float(distractor.value) / self.sum_values

    def is_binary(self):
        for distractor in self.iter_distractors():
            if distractor.value not in [0, self.sum_values]:
                return False
        return True

    def is_correct_answer(self, answer):
        return self.distractors[answer].value == self.sum_values

    def is_partially_correct_answer(self, answer):
        return self.distractors[answer].value > 0

    @classmethod
    def from_aiken(cls, aiken_question):
        gift_question = GiftQuestion(aiken_question.stem)
        correct_answer = aiken_question.correct_answer
        for i, distractor in enumerate(aiken_question.iter_distractors()):
            if i == correct_answer:
                value = 1
            else:
                value = 0
            gift_question.append_distractor(GiftDistractor(distractor, value))
        return gift_question


class GiftQuiz(Quiz):
    def __init__(self, questions=None):
        if questions is None:
            questions = []
        self._lst_questions = questions
        self._default_formatter = DefaultGiftQuizFormatter()

    def append(self, question):
        question.normalize_values()
        self._lst_questions.append(question)

    def iter_questions(self):
        return iter(self._lst_questions)

    def __len__(self):
        return len(self._lst_questions)

    def to_string(self, header="", footer="", formatter=None):
        if formatter is None:
            formatter = self._default_formatter
        s = formatter.to_string(self, header, footer)
        return s

    @classmethod
    def from_aiken(cls, aiken_quiz):
        gift_quiz = GiftQuiz()
        for i, aiken_question in enumerate(aiken_quiz.iter_questions()):
            gift_question = GiftQuestion(aiken_question.stem)
            for j, distractor in enumerate(aiken_question.iter_distractors()):
                if j == aiken_question.correct_answer:
                    value = 1
                else:
                    value = 0
                gift_question.append_distractor(GiftDistractor(distractor, value))
            gift_quiz.append(gift_question)
        return gift_quiz
