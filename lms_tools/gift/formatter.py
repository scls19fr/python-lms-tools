from ..formatter import QuestionFormatter, QuizFormatter
from ._utils import _cleanup, CORRECT_ANSWER_CHAR, WRONG_ANSWER_CHAR


class GiftQuestionFormatter(QuestionFormatter):
    pass


class DefaultGiftQuestionFormatter(GiftQuestionFormatter):
    def to_string(self, question):
        if question.comment is not None and question.comment != "":
            s = "/// %s" % question.comment
        else:
            s = ""
        s += "\n" + "::%s::%s{" % (_cleanup(question.name), _cleanup(question.stem))
        is_bin = question.is_binary()
        sum_values = question.sum_values
        for i, distractor in enumerate(question.iter_distractors()):
            if is_bin:
                if distractor.value == sum_values:
                    c = CORRECT_ANSWER_CHAR
                else:
                    c = WRONG_ANSWER_CHAR
                s += "\n\t%s%s" % (c, distractor.text)
            else:
                val_pct = distractor.value / sum_values * 100.0
                if val_pct != 0:
                    s_val_pct = "%.5f" % val_pct
                else:
                    s_val_pct = "0"
                s += "\n\t%s%s%%%s" % (WRONG_ANSWER_CHAR, s_val_pct, distractor.text)
        s += "\n" + "}"
        return s[1:]


class GiftQuizFormatter(QuizFormatter):
    pass


class DefaultGiftQuizFormatter(GiftQuizFormatter):
    pass
