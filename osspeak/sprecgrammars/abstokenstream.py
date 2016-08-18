from osspeak.sprecgrammars import inputstream
import re

class AbstractTokenStream:

    word_regex = re.compile(r'[a-zA-Z]')

    def __init__(self, text):
        self.stream = inputstream.InputStream(text)
        self.current = None

    def next(self):
        tok = self.current
        self.current = None
        return self.read_next() if tok is None else tok

    def peek(self):
        if self.current is not None:
            return self.current
        self.current = self.read_next()
        return self.current

    def eof(self):
        return self.peek() == None

    def croak(self):
        pass

    def read_while(self, predicate):
        val = ''
        while not self.stream.eof() and predicate(self.stream.peek()):
            val += self.stream.next()
        return val

    def __iter__(self):
        while not self.eof():
            yield self.next()

        #  while (!TokStream.Eof())
        #     {
        #         Token t = TokStream.Next();
        #         ParseToken(t);
        #     }

        # public string ReadWhile(Func<string, bool> predicate)
        # {
        #     var str = "";
        #     while (!Input.Eof() && predicate(Input.Peek()))
        #         str += Input.Next();
        #     return str;
        # }

            # public T Next()
        # {
        #     var tok = Current;
        #     Current = default(T);
        #     return tok != null ? tok : ReadNext();
        # }
        # public T Peek()
        # {
        #     if (Current != null) return Current;
        #     Current = ReadNext();
        #     return Current;
        # }
        # public bool Eof()
        # {
        #     return Peek() == null;
        # }

        # public void Croak(string msg)
        # {
        #     Input.Croak(msg);
        # }