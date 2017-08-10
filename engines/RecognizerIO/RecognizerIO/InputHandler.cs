using System;
using System.IO;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Speech.Recognition;
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

        public bool ProcessIncomingInput(string input)
        {
            /*
            EngManager.LoadGrammar(@"C:\Users\evan\AppData\Local\Temp\249f2b8a-4611-4f3e-b48f-1d694c62ec6b.xml", "foo");
            EngManager.Begin();
            return false;
            */
            dynamic jsonMsg = JsonConvert.DeserializeObject(input);
            string msgType = jsonMsg.Type;
            bool shutdown = false;
            switch (msgType)
            {
                case "load grammars":
                    string grammarXml = jsonMsg.Grammar;
                    string grammarId = jsonMsg.Id;
                    bool startEngine = jsonMsg.StartEngine;
                    string tmpPath = System.IO.Path.GetTempPath() + Guid.NewGuid().ToString() + ".xml";
                    System.IO.File.WriteAllText(tmpPath, grammarXml);
                    EngManager.LoadGrammar(tmpPath, grammarId);
                    System.IO.File.Delete(tmpPath);
                    if (!EngManager.IsRunning && startEngine) EngManager.Begin();
                    break;
                case "load settings":
                    break;
                case "emulate recognition":
                    string text = jsonMsg.Text;
                    EngManager.Engine.EmulateRecognize(text);
                    break;
                case "GET_ENGINE_STATUS":
                    Console.WriteLine(EngManager.Status());
                    break;
                case "shutdown":
                    shutdown = true;
                    break;
                case "start":
                    if (!EngManager.IsRunning) EngManager.Begin();
                    break;
                case "stop":
                    EngManager.Stop();
                    break;
            }
            return shutdown;
        }
    }
    class MainProcessMessage
    {
        public string Type;

    }
}

