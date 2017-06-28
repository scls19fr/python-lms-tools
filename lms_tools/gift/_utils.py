WRONG_ANSWER_CHAR = "~"
CORRECT_ANSWER_CHAR = "="
FEEDBACK_CHAR = "#"


def _cleanup(s):
    for c in list("~=#{}:"):
        s = s.replace(c, "\\" + c)
    return s


class DefaultQuestionNamer():
    def name(self, i, question):
        return "%04d" % (i + 1)
