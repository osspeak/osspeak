class InputStream:

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def next(self):
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def peek(self):
        return None if self.eof() else self.text[self.pos]

    def eof(self):
        return self.pos >= len(self.text)

    def croak(self):
        pass

    