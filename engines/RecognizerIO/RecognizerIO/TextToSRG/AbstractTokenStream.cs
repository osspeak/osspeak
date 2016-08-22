using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TextToSRG
{
    public abstract class AbstractTokenStream<T>
    {

        public InputStream Input;
        public T Current = default(T);


        public AbstractTokenStream(InputStream input)
        {
            Input = input;
        }

        public string ReadWhile(Func<string, bool> predicate)
        {
            var str = "";
            while (!Input.Eof() && predicate(Input.Peek()))
                str += Input.Next();
            return str;
        }

        public bool IsWhitespace(string ch)
        {
            return " \t\n".Contains(ch);
        }

        public T Next()
        {
            var tok = Current;
            Current = default(T);
            return tok != null ? tok : ReadNext();
        }
        public T Peek()
        {
            if (Current != null) return Current;
            Current = ReadNext();
            return Current;
        }
        public bool Eof()
        {
            return Peek() == null;
        }

        public void Croak(string msg)
        {
            Input.Croak(msg);
        }

        public abstract T ReadNext();
    }
}
