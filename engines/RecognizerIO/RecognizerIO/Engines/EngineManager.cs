using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Speech.Recognition;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace RecognizerIO.Engines
{
    class EngineManager
    {
        public SpeechRecognitionEngine Engine;
        public Grammar ActiveGrammar;
        public string GrammarId;
        public string RecognitionGrammarId = "";
        public Boolean IsRunning = false;

        public EngineManager()
        {
            Engine = new SpeechRecognitionEngine();
            Engine.SpeechRecognized += new EventHandler<SpeechRecognizedEventArgs>(recognizer_SpeechRecognized);
            Engine.SpeechDetected += new EventHandler<SpeechDetectedEventArgs>(recognizer_SpeechDetected);
            Engine.RecognizerUpdateReached += new EventHandler<RecognizerUpdateReachedEventArgs>(recognizer_RecognizerUpdateReached);
            Engine.SetInputToDefaultAudioDevice();
        }

        public void LoadGrammar(string path, string grammarId)
        {
            var gram = new Grammar(path);
            if (ActiveGrammar != null)
            {
                Engine.RequestRecognizerUpdate();
            }
            else
            {
                Engine.LoadGrammar(gram);
            }
            ActiveGrammar = gram;
            GrammarId = grammarId;
        }

        void recognizer_SpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {
            HandleRecognition(e.Result);
        }

        void recognizer_SpeechDetected(object sender, SpeechDetectedEventArgs e)
        {
            RecognitionGrammarId = GrammarId;
        }

        void recognizer_RecognizerUpdateReached(object sender, RecognizerUpdateReachedEventArgs e)
        {
            Engine.UnloadAllGrammars();
            Engine.LoadGrammar(ActiveGrammar);
        }

        public void HandleRecognition(RecognitionResult srResult)
        {
            if (srResult == null) return;
            var resultText = srResult.Semantics.Value.ToString().Replace("[object Object]", "");
            var result = new ProcessedRecognitionResult(resultText, srResult.Confidence, RecognitionGrammarId);
            string serializedResult = JsonConvert.SerializeObject(result);
            Console.WriteLine(serializedResult);
        }

        public void Begin()
        {
            Engine.RecognizeAsync(RecognizeMode.Multiple);
            IsRunning = true;
        }

        public void Stop()
        {
            Engine.RecognizeAsyncStop();
            IsRunning = false;
        }

    }
}
