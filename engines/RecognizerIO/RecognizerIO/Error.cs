using System;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RecognizerIO
{
    class Error
    {
        public string Type = "error";
        public string StackTrace;
        public string Message;

        public Error(Exception e)
        {
            StackTrace = e.StackTrace;
            Message = e.Message;
        }
        public void send()
        {
            string serializedError = JsonConvert.SerializeObject(this);
            Console.WriteLine(serializedError);
        }
    }

}
