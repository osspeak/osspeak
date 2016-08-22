using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RecognizerIO
{
    static class ActionParser
    {
        public static List<Action> BuildActions(string actionText)
        {
            var actions = new List<Action>();
            Action actn;
            foreach (char ch in actionText)
            {
                switch (ch)
                {
                    case '`':
                        actn = new Action();
                        break;
                    default:
                        if (!actions.Any() || actions.Last().Type != "SendKeys")
                        {
                            actions.Add(new Action());
                            actions.Last().Type = "SendKeys";
                        }
                        actions.Last().Text += ch;
                        break;
                }
            }
            return actions;
        }
    }
}
