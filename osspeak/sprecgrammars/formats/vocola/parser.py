from osspeak.sprecgrammars import astree, tokens
from osspeak.sprecgrammars.formats.baseparser import BaseParser
from osspeak.sprecgrammars.formats.vocola import voctokstream


class VocolaParser(BaseParser):

    def __init__(self, text):
        super().__init__(text)
        self.stream = voctokstream.VocolaTokenStream(self.text)
        self.grouping_stack = []
        self.parse_map = {
            tokens.WordToken: self.parse_word_token,
            tokens.OrToken: self.parse_or_token,
            tokens.ParenToken: self.parse_paren_token,
        }

    def parse_as_rule(self):
        top_level_rule = astree.Rule()
        self.grouping_stack = [top_level_rule]
        for tok in self.stream:
            self.parse_map[type(tok)](tok)
        return top_level_rule

    def parse_word_token(self, tok):
        word_node = astree.WordNode(tok.text)
        self.grouping_stack[-1].children.append(word_node)

    def parse_or_token(self, tok):
        or_node = astree.OrNode()
        self.grouping_stack[-1].children.append(or_node)

    def parse_paren_token(self, tok):
        pass
