using System;
using System.Collections.Generic;
using System.Speech.Recognition;
using System.Linq;

namespace RecognizerIO.Engines
{
    class ProcessedRecognitionResult
    {
        public string RuleId { get; set; }
        public Dictionary<string, string> Variables;
        public string Type = "result";

        public ProcessedRecognitionResult(RecognitionResult result)
        {
            var root = result.Semantics.First();
            Variables = new Dictionary<string, string>();
            RuleId = root.Key;
            BuildVariables(root.Value);
        }
        /// <summary>
        /// Recurse through result tree to build Variables dictionary
        /// </summary>
        /// <param name="key"></param>
        /// <param name="root"></param>
        private void BuildVariables(SemanticValue root)
        {
            foreach (var semanticResult in root.ToArray())
            {
                Variables[semanticResult.Key] = semanticResult.Value.ToArray().Count() == 0 ? semanticResult.Value.Value.ToString() : "";
                BuildVariables(semanticResult.Value);
            }
        }
    }
}
