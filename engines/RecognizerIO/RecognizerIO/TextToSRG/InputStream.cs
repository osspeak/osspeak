using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TextToSRG
{
    public class InputStream
    {
        
        private string Input;
        private int Pos;

        public InputStream(string input)
        {
            this.Input = input;
            this.Pos = 0;
        }
        public string Next()
        {
            return Input[Pos++].ToString();
        }
        public string Peek()
        {
            return Input.Length > Pos ? Input[Pos].ToString() : "";
        }
        public bool Eof()
        {
            return this.Peek() == "";
        }
        public void Croak(string msg)
        {
            throw new Exception(msg);
        }
    }
}
