using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Speech;
using TextToSRG;

namespace RecognizerIO
{
    class Program
    {
        static void Main(string[] args)
        {
            var inputHandler = new InputHandler();
            while (true)
            {
                var communicatorInput = Console.ReadLine();
                inputHandler.ProcessIncomingInput(communicatorInput);
            }
        }
    }
}
