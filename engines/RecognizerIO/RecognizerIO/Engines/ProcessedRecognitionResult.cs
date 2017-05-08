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
        public string GrammarId;
        public float Confidence;

        public ProcessedRecognitionResult(string semantics, string grammarId, float confidence)
        {
            GrammarId = grammarId;
            Confidence = confidence;
            string[] splitCmds = semantics.Split(new[] { "-command-" }, StringSplitOptions.None).Skip(1).ToArray();
            foreach(var cmd in splitCmds)
            {
                string[] cmdPieces = cmd.Split(':');
                string[] cmdVars = cmdPieces[1].Split('|');
                Commands.Add(new CommandRecognition(cmdPieces[0], cmdVars.Take(cmdVars.Length - 0).ToList()));

            }
        }
    }

    class CommandRecognition
    {
        public string RuleId { get; set; }
        public List<string[]> Variables = new List<string[]>();

        public CommandRecognition(string ruleId, List<string> cmdVars)
        {
            RuleId = ruleId;
            foreach (var cmdVar in cmdVars)
            {
                Variables.Add(cmdVar.Split('='));
            }
        }
    }
}
