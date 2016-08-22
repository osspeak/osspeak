using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace RecognizerIO
{
    class Action
    {


        private string PerformPath = @"C:\Users\evan\modules\net\OSSpeak\CrossUserInput\bin\Debug\CrossUserInput.exe";
        public string Text { get; set; }
        public string Type { get; set; }

        public Action(string type="", string text="")
        {
            Type = type;
            Text = text;
        }
        public void Perform()
        {
            var start = new ProcessStartInfo();
            start.FileName = PerformPath;
            start.Arguments = Type + " " + Text;
            start.UseShellExecute = false;
            return;
            using (Process proc = Process.Start(start))
            {
                proc.WaitForExit();
                var exitCode = proc.ExitCode;
            }
        }
    }
}
