using System;
using RecognizerIO.AudioDevice;
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
        public Boolean IsRunning = false;
        public DeviceEventRaiser eventRaiser;
        public Boolean AudioInputDeviceConnected;

        public EngineManager()
        {
            eventRaiser = new DeviceEventRaiser(this);
            InitEngine();
        }

        void InitEngine() {
            Engine = new SpeechRecognitionEngine();
            Engine.EndSilenceTimeout = TimeSpan.FromSeconds(.5);
            Engine.EndSilenceTimeoutAmbiguous = TimeSpan.FromSeconds(.5);
            Engine.SpeechRecognized += new EventHandler<SpeechRecognizedEventArgs>(recognizer_SpeechRecognized);
            Engine.RecognizerUpdateReached += new EventHandler<RecognizerUpdateReachedEventArgs>(recognizer_RecognizerUpdateReached);
            AudioInputDeviceConnected = false;
            try
            {
                Engine.SetInputToDefaultAudioDevice();
            }
            catch (InvalidOperationException e) {
                Debug.sendMessage("No audio input device detected");
                return;
            }
            AudioInputDeviceConnected = true;
            IsRunning = false;
            if (ActiveGrammar != null)
            {
                Engine.LoadGrammar(ActiveGrammar);
                Begin();
            }
        }

        public void LoadGrammar(Grammar gram, string grammarId)
        {
            gram.Name = grammarId;
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

        void recognizer_RecognizerUpdateReached(object sender, RecognizerUpdateReachedEventArgs e)
        {
            Engine.UnloadAllGrammars();
            Engine.LoadGrammar(ActiveGrammar);
        }

        public void HandleRecognition(RecognitionResult srResult)
        {
            if (srResult == null) return;
            //srResult.Words.ToList()[0].
            var recognizedWords = srResult.Words.Select(x => new RecognizedWord(x.Text)).ToList();
            var result = new ProcessedRecognitionResult(recognizedWords, srResult.Confidence, srResult.Grammar.Name);
            string serializedResult = JsonConvert.SerializeObject(result);
            Console.WriteLine(serializedResult);
        }

        public void ResetDevice()
        {
            Engine.Dispose();
            InitEngine();
        }

        public void Begin()
        {
            Engine.RecognizeAsync(RecognizeMode.Multiple);
            IsRunning = true;
        }

        public void Stop()
        {
            Engine.RecognizeAsyncCancel();
            IsRunning = false;
        }

        public string Status()
        {
            var status = new EngineStatus(GrammarId, IsRunning);
            return JsonConvert.SerializeObject(status);
        }

    }

}
