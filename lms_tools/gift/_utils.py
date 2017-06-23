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


def aiken2gift(aiken_quiz, question_namer=None):
    if question_namer is None:
        question_namer = DefaultQuestionNamer()
    s = ""
    for i, question in enumerate(aiken_quiz.iter_questions()):
        question_text = _cleanup(question.stem)
        question_title = question_namer.name(i, question)
        s += "\n" * 2 + "// question: %d name: %s" % (i + 1, question_title)
        s += "\n" + "::%s::%s{" % (question_title, question_text)
        for j, distractor in enumerate(question.iter_distractors()):
            if question.is_correct_answer(j):
                s += "\n\t" + CORRECT_ANSWER_CHAR + distractor
            else:
                s += "\n\t" + WRONG_ANSWER_CHAR + distractor
        s += "\n" + "}"
    s = s[2:]
    print(s)
    return s
