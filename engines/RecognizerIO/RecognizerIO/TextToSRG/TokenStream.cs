using System;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TextToSRG
{
    class PatternTokenStream : AbstractTokenStream<Token>
    {
        private Regex WordRegex = new Regex(@"[a-zA-Z]");

        public PatternTokenStream(InputStream input) : base(input)
        {
            
        }

        private Token ReadWord()
        {
            var str = ReadWhile((ch) => WordRegex.IsMatch(ch));
            return new WordToken(str);
        }

        private Token ReadParen()
        {
            var ch = Input.Next();
            return new ParenToken(ch == ")");
        }

        private Token ReadOr()
        {
            var ch = Input.Next();
            return new OrToken();
        }

        public override Token ReadNext()
        {
            ReadWhile(IsWhitespace);
            if (Input.Eof() == true) return null;
            string ch = Input.Peek();
            if (WordRegex.IsMatch(ch)) return ReadWord();
            if (ch == "(" || ch == ")") return ReadParen();
            if (ch == "|") return ReadOr();
            Croak("Invalid Character: " + ch);
            return null;
        }
     
    }
}
