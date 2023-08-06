
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.if_statement.if_keyword)


class rule_025(token_case):
    '''
    Checks the "if" keyword has proper case.
    '''

    def __init__(self):
        token_case.__init__(self, 'if', '025', lTokens)
