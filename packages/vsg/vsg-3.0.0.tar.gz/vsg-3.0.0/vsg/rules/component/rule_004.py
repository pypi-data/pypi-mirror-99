
from vsg.rules import token_case

from vsg import token

lTokens = []
lTokens.append(token.component_declaration.component_keyword)


class rule_004(token_case):
    '''
    Component rule 004 checks the "component" keyword has proper case.
    '''

    def __init__(self):
        token_case.__init__(self, 'component', '004', lTokens)
