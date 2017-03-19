using System;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Speech;

namespace RecognizerIO
{
    class Program
    {
        static void Main(string[] args)
        {
            var inputHandler = new InputHandler();
            bool shutdown = false;
            while (!shutdown)
            {
                try
                {
                    var communicatorInput = Console.ReadLine();
                    shutdown = inputHandler.ProcessIncomingInput(communicatorInput);
                }
                catch (Exception e)
                {
                    var error = new Error(e);
                    string serializedError = JsonConvert.SerializeObject(error);
                    Console.WriteLine(serializedError);
                    throw;
                }
            }
        }
    }
}
