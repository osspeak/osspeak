using System;
using System.IO;
using Newtonsoft.Json;
using System.Xml;
using System.Collections.Generic;
using System.Speech.Recognition;
using System.Speech.Recognition.SrgsGrammar;
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
        }

        public bool ProcessIncomingInput(string input)
        {
            bool shutdown = false;
            dynamic jsonMsg = JsonConvert.DeserializeObject(input);
            string msgType = jsonMsg.Type;
            switch (msgType)
            {
                case "LOAD_ENGINE_GRAMMAR":
                    string grammarXml = jsonMsg.Grammar;
                    string grammarId = jsonMsg.Id;
                    bool startEngine = jsonMsg.StartEngine;
                    using (var strReader = new StringReader(grammarXml))
                    using (XmlReader xmlReader = XmlReader.Create(strReader))
                    {
                        var document = new SrgsDocument(xmlReader);
                        var grammar = new Grammar(document);
                        EngManager.LoadGrammar(grammar, grammarId);
                    }
                    if (!EngManager.IsRunning && EngManager.AudioInputDeviceConnected && startEngine) EngManager.Begin();
                    break;
                case "LOAD_SETTINGS":
                    Debug.sendMessage("Loading settings from message" + input);
                    break;
                case "SET_ENGINE_SETTINGS":
                    dynamic endSilenceTimeout = jsonMsg.Settings.end_silence_timeout;
                    dynamic endSilenceTimeoutAmbiguous = jsonMsg.Settings.end_silence_timeout_ambiguous;
                    if (endSilenceTimeout != null) {
                        EngManager.Engine.EndSilenceTimeout = TimeSpan.FromSeconds(Convert.ToDouble(endSilenceTimeout));
                    }
                    if (endSilenceTimeoutAmbiguous != null) {
                        EngManager.Engine.EndSilenceTimeoutAmbiguous = TimeSpan.FromSeconds(Convert.ToDouble(endSilenceTimeoutAmbiguous));
                    }
                    break; // {"Type": "SET_ENGINE_SETTINGS", "Settings": {"end_silence_timeout": "5"}}
                case "EMULATE_RECOGNITION_EVENT":
                    string text = jsonMsg.Text;
                    EngManager.Engine.EmulateRecognize(text);
                    break;
                case "GET_ENGINE_STATUS":
                    Console.WriteLine(EngManager.Status());
                    break;
                case "ENGINE_SHUTDOWN":
                    shutdown = true;
                    break;
                case "RESET_DEVICE":
                    EngManager.ResetDevice();
                    break;
                case "ENGINE_START":
                    if (!EngManager.IsRunning && EngManager.AudioInputDeviceConnected) EngManager.Begin();
                    break;
                case "ENGINE_STOP":
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

