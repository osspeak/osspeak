using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Speech.Recognition;
using System.Threading.Tasks;

namespace TextToSRG
{
    public abstract class ASTNode
    {

    }

    public class ExpressionNode : ASTNode
    {
        public bool Closed;
        public List<ASTNode> ChildNodes;

        public ExpressionNode()
        {
            Closed = false;
            ChildNodes = new List<ASTNode>();

        }
        public GrammarBuilder ToGrammarBuilder()
        {
            bool orFlag = false;
            var children = new List<GrammarBuilder>();
            foreach (ASTNode child in ChildNodes)
            {
                string nodeType = child.GetType().ToString();
                if (nodeType == "TextToSRG.OrNode")
                {
                    orFlag = true;
                    continue;
                }
                switch (nodeType)
                {
                    case "TextToSRG.ExpressionNode":
                        var expressionGb = (child as ExpressionNode).ToGrammarBuilder();
                        // if no GrammarBuilder exists or previous node was OrNode, add new GrammarBuider
                        // Otherwise, append to end of last GrammarBuilder
                        if (!children.Any() || orFlag)
                        {
                            children.Add(expressionGb);
                        }
                        else
                        {
                            children.Last().Append(expressionGb);
                        }
                        break;
                    case "TextToSRG.WordNode":
                        string wordText = (child as WordNode).Text;
                        if (!children.Any() || orFlag)
                        {
                            var wordGb = new GrammarBuilder(wordText);
                            children.Add(wordGb);
                        }
                        else
                        {
                            children.Last().Append(wordText);
                        }
                        break;
                }
                orFlag = false;
            }
            return new GrammarBuilder(new Choices(children.ToArray()));
        }
    }

    public class OrNode : ASTNode
    {
        public OrNode()
        {
            
        }

    }

    public class WordNode : ASTNode
    {
        public string Text;

        public WordNode(string text)
        {
            Text = text;
        }

    }
}
