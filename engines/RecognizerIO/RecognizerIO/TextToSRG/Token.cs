using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using TextToSRG;
using System.Threading.Tasks;

namespace TextToSRG
{
    abstract public class Token
    {

        public Token()
        {
        }
    }

    public class WordToken : Token
    {

        public string Text;

        public WordToken(string text)
        {
            Text = text;
        }
    }

    public class ParenToken : Token
    {

        public bool IsClose;

        public ParenToken(bool isClose)
        {
            IsClose = isClose;
        }
    }

    public class OrToken : Token
    {

        public OrToken()
        {

        }
    }

    public class RepeatToken : Token
    {

        public RepeatToken()
        {

        }
    }

    public class NumberRangeToken : Token
    {

        public int Start { get; set; }
        public int Stop { get; set; }
        public int Step { get; set; }


        public NumberRangeToken()
        {

        }
    }

}
