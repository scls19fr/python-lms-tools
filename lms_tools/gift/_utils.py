from enum import Enum


GiftParserState = Enum("GiftParserState", "START STEM DISTRACTORS END_OF_QUESTION")

WRONG_ANSWER_CHAR = "~"
CORRECT_ANSWER_CHAR = "="
FEEDBACK_CHAR = "#"

SPECIAL_CHARS = "~=#{}:"

COMMENT_PATTERN = "^\/\/(.*)$"
STEM_PATTERN = "^::(.*)::(.*){$"
DISTRACTORS_PATTERN = "^\s*([=|~])\s*(.*)$"
END_OF_QUESTION_PATTERN = "(.*)}$"


def _escape_special_chars(s):
    for c in list(SPECIAL_CHARS):
        s = s.replace(c, "\\" + c)
    return s


def _unescape_special_chars(s):
    for c in list(SPECIAL_CHARS):
        s = s.replace("\\" + c, c)
    return s


class DefaultQuestionNamer():
    def name(self, i, question):
        return "%04d" % (i + 1)
