using System;
using System.Collections.Generic;
using System.Speech.Recognition;
using System.Linq;

namespace RecognizerIO.Engines
{
    class ProcessedRecognitionResult
    {
        public string GrammarId;
        public string Type = "recognition";
        public float Confidence;
        public List<RecognizedWord> Words;

        public ProcessedRecognitionResult(List<RecognizedWord> words, float confidence, string grammarId)
        {
            Confidence = confidence;
            GrammarId = grammarId;
            Words = words;
        }
    }

    class RecognizedWord
    {
        public string Text { get; set; }

        public RecognizedWord(string text)
        {
            Text = text;
        }
    }

}