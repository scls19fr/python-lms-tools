from ..formatter import QuestionFormatter, QuizFormatter
from .distractor import DefaultDistractorKeyParser


class AikenQuestionFormatter(QuestionFormatter):
    pass


class DefaultAikenQuestionFormatter(AikenQuestionFormatter):
    def __init__(self, distractor_key_parser=None):
        if distractor_key_parser is None:
            distractor_key_parser = DefaultDistractorKeyParser()
        self._distractor_key_parser = distractor_key_parser

    def to_string(self, question):
        s = question.stem
        for i, distractor in enumerate(question.iter_distractors()):
            s += "\n%s) " % self._distractor_key_parser.to_string(i) + distractor
        s += "\n" + "ANSWER: %s" % self._distractor_key_parser.to_string(question.correct_answer)
        return s


class AikenQuizFormatter(QuizFormatter):
    pass


class DefaultAikenQuizFormatter(AikenQuizFormatter):
    pass
