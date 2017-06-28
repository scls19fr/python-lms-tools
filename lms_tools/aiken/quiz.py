from ..base import Quiz, Question
from ..exception import ParseException
from ._utils import AikenParserState, DISTRACTORS_PATTERN, CORRECT_ANSWER_PATTERN
from .formatter import DefaultAikenQuizFormatter, DefaultAikenQuestionFormatter
from .distractor import DefaultDistractorKeyParser

import re


class AikenQuestion(Question):
    def __init__(self, stem="", distractors=None, correct_answer=None):
        self.stem = stem
        if distractors is None:
            distractors = []
        self.distractors = distractors
        self.correct_answer = correct_answer
        self._default_formatter = DefaultAikenQuestionFormatter()

    def append_stem(self, line):
        if self.stem == "":
            self.stem = line
        else:
            self.stem = self.stem + "\n" + line

    def append_distractor(self, line):
        self.distractors.append(line)

    def set_correct_answer(self, correct_answer, distractor_key_parser=None):
        if distractor_key_parser is None:
            distractor_key_parser = DefaultDistractorKeyParser()
        if not isinstance(correct_answer, int):
            correct_answer = distractor_key_parser.to_int(correct_answer)
        assert correct_answer < len(self.distractors), ValueError("correct_answer must be lower than len(distractors)")
        self.correct_answer = correct_answer

    def is_correct_answer(self, answer):
        return answer == self.correct_answer

    @classmethod
    def parse(cls, s):
        quiz = AikenQuiz.parse(s)
        assert len(quiz) == 1, ParseException("quiz doesn't have only one question")
        return quiz._lst_questions[0]

    @classmethod
    def from_gift(cls, gift_question):
        assert gift_question.is_binary()
        aiken_question = AikenQuestion(gift_question.stem)
        sum_values = gift_question.sum_values
        for i, distractor in enumerate(gift_question.iter_distractors()):
            aiken_question.append_distractor(distractor.text)
            if distractor.value == sum_values:
                aiken_question.set_correct_answer(i)
        return aiken_question


class AikenQuiz(Quiz):
    def __init__(self, questions=None):
        if questions is None:
            questions = []
        self._lst_questions = questions
        self._default_formatter = DefaultAikenQuizFormatter()

    def append(self, question):
        self._lst_questions.append(question)

    def iter_questions(self):
        return iter(self._lst_questions)

    def __len__(self):
        return len(self._lst_questions)

    def to_string(self, header="", footer="", formatter=None):
        if formatter is None:
            formatter = self._default_formatter
        s = formatter.to_string(self, header="", footer="", )
        return s

    @classmethod
    def parse(cls, s, strict=True):
        def is_distractor(line):
            return re.match(DISTRACTORS_PATTERN, line) is not None

        def split_distractor(line):
            key, distractor = re.findall(DISTRACTORS_PATTERN, line)[0]
            return key, distractor

        def is_correct_answer(line):
            return re.match(CORRECT_ANSWER_PATTERN, line) is not None

        def get_correct_answer(line):
            correct_answer = re.findall(CORRECT_ANSWER_PATTERN, line)[0]
            return correct_answer

        state = AikenParserState.START
        quiz = AikenQuiz()
        for line in s.splitlines():
            if state in [AikenParserState.START, AikenParserState.CORRECT_ANSWER]:
                if not is_distractor(line) and not is_correct_answer(line):
                    q = AikenQuestion(line)
                    state = AikenParserState.STEM
                else:
                    raise ParseException("Line %r should be a stem" % line)
            elif state == AikenParserState.STEM:
                if not is_distractor(line) and not is_correct_answer(line):
                    q.append_stem(line)
                else:
                    if is_distractor(line):
                        key, distractor = split_distractor(line)
                        # assert increasing keys
                        q.append_distractor(distractor)
                        state = AikenParserState.DISTRACTORS
                    else:
                        raise ParseException("Line %r should be a distractor" % line)
            elif state == AikenParserState.DISTRACTORS:
                if is_correct_answer(line):
                    correct_answer = get_correct_answer(line)
                    q.set_correct_answer(correct_answer)
                    quiz.append(q)
                    state = AikenParserState.CORRECT_ANSWER
                elif is_distractor(line):
                    key, distractor = split_distractor(line)
                    # assert increasing keys
                    q.append_distractor(distractor)
                else:
                    if strict:
                        raise ParseException("Line %r can't be parsed (should be distractor or correct answer)" % line)
                    else:
                        q.append_stem(line)
            else:
                raise ParseException("Unknown state %s" % state)
        return quiz

    @classmethod
    def from_gift(cls, gift_quiz):
        raise NotImplementedError
