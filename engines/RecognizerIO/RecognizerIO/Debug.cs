using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace RecognizerIO
{
    class Debug
    {
        public static void sendMessage(string msg, string msgType="DEBUG")
        {
            var debugMsg = new DebugMessage(msgType, msg);
            string serializedError = JsonConvert.SerializeObject(debugMsg);
            Console.WriteLine(serializedError);
        }
    }

    class DebugMessage
    {
        public string Type;
        public string Message;

        public DebugMessage(string msgType, string msg)
        {
            Type = msgType;
            Message = msg;
        }

    }
}
