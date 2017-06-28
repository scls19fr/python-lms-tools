class Formatter():
    pass


class QuestionFormatter(Formatter):
    pass


class QuizFormatter(Formatter):
    def to_string(self, quiz, header="", footer=""):
        s = ""
        for i, q in enumerate(quiz.iter_questions()):
            if i == 0:
                s = q.to_string()
            else:
                s += "\n\n" + q.to_string()
        if header != "":
            s = header + "\n" + s
        if footer != "":
            s = s + "\n" + footer
        return s
