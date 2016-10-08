using System;
using System.Collections.Generic;
using System.Speech.Recognition;
using System.Linq;

namespace RecognizerIO.Engines
{
    class ProcessedRecognitionResult
    {
        public List<CommandRecognition> Commands = new List<CommandRecognition>();
        public string Type = "recognition";

        public ProcessedRecognitionResult(SemanticValue semantics)
        {
            foreach(var cmdResult in semantics)
            {
                var recognition = new CommandRecognition(cmdResult.Value, cmdResult.Key);
                Commands.Add(recognition);
            }
            var root = "4";
        }
    }

    class CommandRecognition
    {
        public string RuleId { get; set; }
        public Dictionary<string, string> Variables = new Dictionary<string, string>();

        public CommandRecognition(SemanticValue cmdMatch, string ruleId)
        {
            RuleId = ruleId;
            BuildVariables(cmdMatch);
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
                if (semanticResult.Key[0] == 'r')
                {
                    Variables[semanticResult.Key] = semanticResult.Value.ToArray().Count() == 0 ? semanticResult.Value.Value.ToString() : "";
                }
                BuildVariables(semanticResult.Value);
            }
        }
    }
}
