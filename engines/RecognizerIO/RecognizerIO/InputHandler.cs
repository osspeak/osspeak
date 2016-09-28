using System;
using Newtonsoft.Json;
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
            dynamic jsonMsg = JsonConvert.DeserializeObject(input);
            string msgType = jsonMsg.Type;
            switch (msgType)
            {
                case "load grammar":
                    string xmlPath = jsonMsg.path;
                    EngManager.LoadGrammar(xmlPath);
                    EngManager.Begin();
                    break;
            }
        }
    }
    class MainProcessMessage
    {
        public string Type;

    }
}

