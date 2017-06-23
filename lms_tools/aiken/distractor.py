class AbstractDistractorKeyParser():
    pass


class AbstractLetterDistractorKeyParser(AbstractDistractorKeyParser):
    @classmethod
    def to_int(self, c):
        n = ord(c.upper()) - ord('A')
        if n < 26:
            return n
        else:
            raise NotImplementedError("char %r is not a possible answer" % c)


class UpperedLetterDistractorKeyParser(AbstractLetterDistractorKeyParser):
    @classmethod
    def to_string(self, n):
        c = chr(65 + n)
        return c


class LoweredLetterDistractorKeyParser(AbstractLetterDistractorKeyParser):
    @classmethod
    def to_string(self, n):
        c = chr(ord('A') + n)
        return c


class DefaultDistractorKeyParser(UpperedLetterDistractorKeyParser):
    pass
