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
            //EngManager.LoadGrammar(@"C:\Users\evan\AppData\Local\Temp\8da0e5d7-f8ea-4b87-bb58-6aff4c735606.xml");
        }
        //{"Type": "load grammars", "Init": true, "Grammars": {"foo": "<grammar mode=\"voice\" root=\"r28a91f8b02df47519b30a27ebe6a442d\" tag-format=\"semantics/1.0\" version=\"1.0\" xml:lang=\"en-US\" xmlns=\"http://www.w3.org/2001/06/grammar\"><rule id =\"r28a91f8b02df47519b30a27ebe6a442d\"><item repeat=\"1-\"><one-of><item><ruleref uri=\"#re91410181e2e424884ee05bf40fbae3c\" /><tag>out.re91410181e2e424884ee05bf40fbae3c=rules.re91410181e2e424884ee05bf40fbae3c;</tag></item></one-of></item></rule><rule id =\"re91410181e2e424884ee05bf40fbae3c\"><one-of><item>bar</item></one-of></rule></grammar>", "bar": "<grammar mode=\"voice\" root=\"rd095b61c5ab448209cb6b7bdfb975fa7\" tag-format=\"semantics/1.0\" version=\"1.0\" xml:lang=\"en-US\" xmlns=\"http://www.w3.org/2001/06/grammar\"><rule id=\"rd095b61c5ab448209cb6b7bdfb975fa7\"><item repeat=\"1-\"><one-of><item><ruleref uri=\"#rf7101cd8b2b748cf95ee7f921d2437fa\" /><tag>out.rf7101cd8b2b748cf95ee7f921d2437fa=rules.rf7101cd8b2b748cf95ee7f921d2437fa;</tag></item></one-of></item></rule><rule id =\"r26cbf9b7af554304bc5226c6676330d9\"><one-of><item>a</item><item>b</item><item>c</item></one-of></rule><rule id=\"rf7101cd8b2b748cf95ee7f921d2437fa\"><one-of><item><item><ruleref uri =\"#r26cbf9b7af554304bc5226c6676330d9\" /><tag>out.r26cbf9b7af554304bc5226c6676330d9=rules.r26cbf9b7af554304bc5226c6676330d9;</tag></item></item></one-of></rule></grammar>"}}
        public void ProcessIncomingInput(string input)
        {
            var p = @"C:\Users\evan\AppData\Local\Temp\tmpovlw8elw";
            using (StreamReader sr = new StreamReader(p))
            {
                input = sr.ReadToEnd();
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
                    //if (init) EngManager.Begin();
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

