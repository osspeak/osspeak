using System;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TextToSRG;

namespace RecognizerIO
{
    class ActionTokenStream : AbstractTokenStream<Action>
    {
        private Regex WordRegex = new Regex(@"[a-zA-Z]");

        public ActionTokenStream(InputStream input) : base(input)
        {
            Current = null;
        }

        public Action ReadLiteral()
        {
            string text = "";
            string defaultError = "end of file";
            string error = defaultError;
            while (!Input.Eof() && error == defaultError)
            {
                var ch = Input.Next();
                switch (ch)
                {
                    case "\\":
                        if (Input.Eof()) error = "asd";
                        text += Input.Next();
                        break;
                    case "{":
                        text += "{{";
                        break;
                    case "}":
                        text += "}}";
                        break;
                    case "\"":
                        return new Action("Literal", text);
                    default:
                        text += ch;
                        break;
                }
            }
            Croak(error);
            return null;
        }

        public override Action ReadNext()
        {
            ReadWhile(IsWhitespace);
            if (Input.Eof() == true) return null;
            string ch = Input.Peek();
            if (ch == "\"") return ReadLiteral();
            Croak("Invalid Character: " + ch);
            return null;
        }

    }
}
