using System;
using System.IO;
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
            //EngManager.LoadGrammar(@"C:\Users\evan\AppData\Local\Temp\1a2f4100-8b3f-47f5-a3f2-ca79d282682b.xml");
        }

        public void ProcessIncomingInput(string input)
        {
            /*
            EngManager.LoadGrammar(@"C:\Users\evan\AppData\Local\Temp\17b78875-79f8-4335-aa92-f826dbdcb7b4.xml");
            EngManager.Begin();
            return;
            */
            var p = @"C:\Users\evan\AppData\Local\Temp\tmpovlw8elw";
            using (StreamReader sr = new StreamReader(p))
            {
                //input = sr.ReadToEnd();
            }
            dynamic jsonMsg = JsonConvert.DeserializeObject(input);
            string msgType = jsonMsg.Type;
            switch (msgType)
            {
                case "load grammars":
                    var grammars = jsonMsg.Grammars.ToObject<Dictionary<string, string>>();
                    foreach(var item in grammars)
                    {
                        string xml = item.Value;
                        string tmpPath = System.IO.Path.GetTempPath() + Guid.NewGuid().ToString() + ".xml";
                        System.IO.File.WriteAllText(tmpPath, xml);
                        EngManager.LoadGrammar(tmpPath);
                        //System.IO.File.Delete(tmpPath);
                    }
                    bool init = jsonMsg.Init;
                    if (init) EngManager.Begin();
                    break;
                case "load settings":
                    break;
            }
        }
    }
    class MainProcessMessage
    {
        public string Type;

    }
}

