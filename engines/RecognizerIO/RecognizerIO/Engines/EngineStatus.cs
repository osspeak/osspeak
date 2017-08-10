using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RecognizerIO.Engines
{
    class EngineStatus
    {
        public string GrammarId { get; set; }
        public string Type { get; set; } = "SET_ENGINE_STATUS";
        public bool IsRunning { get; set; }

        public EngineStatus(string grammarId, bool isRunning)
        {
            GrammarId = grammarId;
            IsRunning = isRunning;
        }
    }

}
