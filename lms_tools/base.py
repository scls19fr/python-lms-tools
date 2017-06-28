class Question():
    def __len__(self):
        return len(self.distractors)

    def iter_distractors(self):
        return iter(self.distractors)

    def to_string(self, formatter=None):
        if formatter is None:
            formatter = self._default_formatter
        s = formatter.to_string(self)
        return s


class Quiz():
    @classmethod
    def join(cls, lst_quiz):
        quiz_result = cls()
        for quiz in lst_quiz:
            for question in quiz.iter_questions():
                quiz_result.append(question)
        return quiz_result
