using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TextToSRG
{
    public class Api
    {
        public static ExpressionNode TextToAST(string commandString)
        {
            var p = new Parser();
            ExpressionNode astRoot = p.ParseTopLevel(commandString);
            return astRoot;
        }
    }
}
