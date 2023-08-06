
from vsg.rules import split_line_at_token

from vsg import token

lTokens = []
lTokens.append(token.if_statement.end_keyword)


class rule_020(split_line_at_token):
    '''
    Moves code after the is keyword to the next line.
    '''

    def __init__(self):
        split_line_at_token.__init__(self, 'if', '020', lTokens)
        self.solution = 'Move *end if* keywords to their own line.'
