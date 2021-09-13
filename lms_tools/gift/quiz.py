from ..base import Quiz, Question
from .formatter import DefaultGiftQuizFormatter, DefaultGiftQuestionFormatter
from ..exception import ParseException
from ._utils import (GiftParserState, COMMENT_PATTERN, STEM_PATTERN,
                     DISTRACTORS_PATTERN, END_OF_QUESTION_PATTERN)

import re


class GiftDistractor():
    def __init__(self, text, value=0, feedback=""):
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

    def append_stem(self, line):
        if self.stem == "":
            self.stem = line
        else:
            self.stem = self.stem + "\n" + line

    def append_distractor(self, distractor):
        if not isinstance(distractor, GiftDistractor):
            distractor = GiftDistractor(distractor)
        self.distractors.append(distractor)

    @property
    def sum_values(self):
        result = 0
        for distractor in self.iter_distractors():
            result += distractor.value
        return result

    def normalize_values(self):
        if self.sum_values != 0:
            for distractor in self.iter_distractors():
                distractor.value = float(distractor.value) / self.sum_values

    def is_binary(self):
        for distractor in self.iter_distractors():
            if distractor.value not in [0, self.sum_values]:
                return False
        return True

    def set_correct_answer(self, answer, value=1):
        self.distractors[answer].value = value

    def is_correct_answer(self, answer):
        return self.distractors[answer].value == self.sum_values

    def is_partially_correct_answer(self, answer):
        return self.distractors[answer].value > 0

    def is_incorrect_answer(self, answer):
        return self.distractors[answer].value <= 0

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

    @classmethod
    def parse(cls, s):
        quiz = GiftQuiz.parse(s)
        assert len(quiz) == 1, ParseException("quiz doesn't have only one question")
        return quiz._lst_questions[0]


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

    def is_binary(self):
        for question in self.iter_questions():
            if not question.is_binary():
                return False
        return True

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

    @classmethod
    def parse(cls, s):
        def is_comment(line):
            return re.match(COMMENT_PATTERN, line) is not None

        def is_empty(line):
            return line == ""

        def is_stem(line):
            return re.match(STEM_PATTERN, line) is not None

        def split_stem(line):
            name, stem = re.findall(STEM_PATTERN, line)[0]
            return name, stem

        def is_distractor(line):
            return re.match(DISTRACTORS_PATTERN, line) is not None

        def split_distractor(line):
            key, distractor = re.findall(DISTRACTORS_PATTERN, line)[0]
            # ToDo feedback
            return key, distractor

        def is_end_of_question(line):
            return re.match(END_OF_QUESTION_PATTERN, line) is not None

        def before_end_of_question(line):
            return re.findall(END_OF_QUESTION_PATTERN, line)[0]

        state = GiftParserState.START
        quiz = GiftQuiz()
        for line in s.splitlines():
            if is_comment(line) or is_empty(line):
                continue

            if state in [GiftParserState.START, GiftParserState.END_OF_QUESTION]:
                if is_stem(line):
                    name, stem = split_stem(line)
                    q = GiftQuestion(stem, name=name)
                    state = GiftParserState.STEM
                else:
                    raise ParseException("Line %r should be a stem" % line)
            elif state in [GiftParserState.STEM, GiftParserState.DISTRACTORS]:
                if not (is_distractor(line) or is_end_of_question(line)):
                    q.append_stem(line)
                else:
                    if is_end_of_question(line):
                        pre_line = before_end_of_question(line)  # noqa
                        # process pre_line
                        state = GiftParserState.END_OF_QUESTION
                        quiz.append(q)
                    elif is_distractor(line):
                        key, distractor = split_distractor(line)
                        if key == "=":
                            value = 1
                        elif key == "~":
                            value = 0
                        else:
                            # ToDo: get value
                            raise NotImplementedError("unsupported distractor value %r" % line)
                        q.append_distractor(GiftDistractor(distractor, value))
                        state = GiftParserState.DISTRACTORS
                    else:
                        raise ParseException("Line %r should be a distractor" % line)
            else:
                raise ParseException("Unknown state %s" % state)
        return quiz

    def to_xml(self, *args, **kwargs):
        return self.to_xml_moodle(*args, **kwargs)

    def to_xml_moodle(self, category='', shuffleanswers=False):
        from yattag import Doc, indent

        doc, tag, text = Doc().tagtext()
        doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
        with tag('quiz'):
            if category != '':
                with tag('question', type='category'):
                    with tag('category'):
                        with tag('text'):
                            text(category)
        for question in self.iter_questions():
            with tag('question', type='multichoice'):
                with tag('name'):
                    with tag('text'):
                        text(question.name)
                with tag('questiontext'):
                    with tag('text'):
                        text(question.stem)
                with tag('shuffleanswers'):
                    text(str(shuffleanswers).lower())
                for distractor in question.iter_distractors():
                    value_pct = distractor.value * 100
                    if value_pct == 100.0:
                        value_pct = 100
                    elif value_pct == 0.0:
                        value_pct = 0
                    with tag('answer', fraction=value_pct):
                        with tag('text'):
                            text(distractor.text)
        return indent(doc.getvalue())
