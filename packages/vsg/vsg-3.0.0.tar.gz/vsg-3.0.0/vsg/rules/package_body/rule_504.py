
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.package_body.end_keyword)


class rule_504(token_case):
    '''
    Checks the "body" keyword has proper case.
    '''

    def __init__(self):
        token_case.__init__(self, 'package_body', '504', lTokens)
