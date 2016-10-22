using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Speech.Recognition;
using Newtonsoft.Json;
using TextToSRG;
using System.Threading.Tasks;

namespace RecognizerIO.Engines
{
    class EngineManager
    {
        public SpeechRecognitionEngine Engine;
        public Grammar RootGrammar;
        private CommandLoader CmdLoader;

        public EngineManager()
        {
            Engine = new SpeechRecognitionEngine();
            Engine.SpeechRecognized += new EventHandler<SpeechRecognizedEventArgs>(recognizer_SpeechRecognized);
            Engine.SetInputToDefaultAudioDevice();
        }

        public void LoadGrammar(string path)
        {
            var gram = new Grammar(path);
            Engine.LoadGrammar(gram);
        }

        void recognizer_SpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {   
            HandleRecognition(e.Result);
        }

        public void HandleRecognition(RecognitionResult srResult)
        {
            if (srResult == null || srResult.Confidence <= .9) return;
            var resultText = srResult.Semantics.Value.ToString().Replace("[object Object]", "");
            var result = new ProcessedRecognitionResult(resultText);
            string serializedResult = JsonConvert.SerializeObject(result);
            Console.WriteLine(serializedResult);
        }

        public void Begin()
        {
            Engine.RecognizeAsync(RecognizeMode.Multiple);
        }

        public void Stop()
        {
            Engine.RecognizeAsyncCancel();
        }

    }
}
