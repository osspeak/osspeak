using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RecognizerIO
{
    class InputHandler { 

        public Engines.EngineManager EngManager { get; set; }


        public InputHandler()
        {
            EngManager = new Engines.EngineManager();
            //EngManager.LoadGrammar(@"C:\Users\evan\AppData\Local\Temp\8da0e5d7-f8ea-4b87-bb58-6aff4c735606.xml");
        }

        public void ProcessIncomingInput(string input)
        {
            var splitInput = input.Split(' ');
            switch (splitInput[0])
            {
                case "grammar_content":
                    string xml = String.Join(" ", splitInput.Skip(1).ToArray());
                    string tmpPath = System.IO.Path.GetTempPath() + Guid.NewGuid().ToString() + ".xml";
                    System.IO.File.WriteAllText(tmpPath, xml);
                    tmpPath = @"C:\Users\evan\AppData\Local\Temp\44af39ec-f439-4645-8e0a-a27b1097ce0f.xml";
                    EngManager.LoadGrammar(tmpPath);
                    EngManager.Begin();
                    //System.IO.File.Delete(tmpPath);
                    break;
            }
        }
    }
}
//grammar_content