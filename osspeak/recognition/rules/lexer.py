import re
from inspect import isclass
from recognition.rules import tokens

TOKEN_PATTERNS = tuple((re.compile(p, re.I), _) for p, _ in (
    (r'[\n\t ]+', tokens.WhitespaceToken),
    (r'[a-z0-9]+', tokens.WordToken),
    (r'=.+', lambda text, stream: tokens.ActionSubstituteToken(text[1:], stream.defined_functions)),
    (r'<[a-z_]+[a-z0-9_]*>', lambda text, _: tokens.NamedRuleToken(text[1:-1])),
    (r'_((\d*-\d*)|\d+)', lambda text, stream: stream.read_repetition(text[1:])),
    (r'\|', tokens.OrToken),
    (r'\(', tokens.GroupingOpeningToken),
    (r'\)', tokens.GroupingClosingToken),
    (r'\[', tokens.OptionalGroupingOpeningToken),
    (r'\]', tokens.OptionalGroupingClosingToken),
))

class RuleLexer:

    def __init__(self, text, defined_functions=None):
        self.text = text
        self.defined_functions = {} if defined_functions is None else defined_functions

    def read_repetition(self, text):
        '''
        Ex: left_3 or (hello|goodbye)_3-9 for inclusive ranges
        Dash indicates range, low/high both optional, low defaults to
        0, high defaults to infinity
        '''
        assert text
        if '-' not in text:
            low, high = text, text
        else:
            low, high = text.split('-')
            low = low or 0
            high = high or None
        return tokens.RepetitionToken(low=low, high=high)

    def read_next_token(self, pos):
        for pattern, token_creator in TOKEN_PATTERNS:
            match = pattern.match(self.text, pos=pos) 
            if match:
                matched_text = self.text[pos:match.span()[-1]]
                token = token_creator(matched_text) if isclass(token_creator) else token_creator(matched_text, self)
                if hasattr(token, 'consumed_char_count'):
                    pos += token.consumed_char_count + 1
                else:
                    pos = match.span()[-1]
                return token, pos
        self.croak(f'Cannot tokenize text: {self.text[pos:]}')

    def __iter__(self):
        pos = 0
        while pos < len(self.text):
            token, pos = self.read_next_token(pos)
            yield token
