
from vsg import parser


def is_token_at_start_of_line(iIndex, oTokenMap):
    if oTokenMap.is_token_at_index(parser.carriage_return, iIndex - 1):
        return True
    if oTokenMap.is_token_at_index(parser.carriage_return, iIndex - 2) and oTokenMap.is_token_at_index(parser.whitespace, iIndex - 1):
        return True
    return False


def is_token_at_end_of_line(iIndex, oTokenMap):
    if oTokenMap.is_token_at_index(parser.carriage_return, iIndex + 1):
        return True
    if oTokenMap.is_token_at_index(parser.comment, iIndex + 1):
        return True
    if oTokenMap.is_token_at_index(parser.whitespace, iIndex + 1):
        if oTokenMap.is_token_at_index(parser.carriage_return, iIndex + 2):
            return True
        if oTokenMap.is_token_at_index(parser.comment, iIndex + 2):
            return True
    return False


def get_indexes_of_token_list(lTokens, oTokenMap):
    lReturn = []
    for oToken in lTokens:
        lReturn.extend(oTokenMap.get_token_indexes(oToken))

    lReturn.sort()

    return lReturn


def get_line_numbers_of_indexes_in_list(lIndexes, oTokenMap):
    lReturn = []
    for iIndex in lIndexes:
        lReturn.append(oTokenMap.get_line_number_of_index(iIndex))

    lReturn.sort()

    return lReturn


def is_index_between_indexes(iIndex, lStart, lEnd, bInclusive=False):
    for iStart, iEnd in zip(lStart, lEnd):
        if bInclusive:
            if iStart <= iIndex and iIndex <= iEnd:
                return True
        else:
            if iStart < iIndex and iIndex < iEnd:
                return True
    return False


def filter_indexes_which_start_a_line(oToken, oTokenMap):
    lReturn = []
    lTemp = oTokenMap.get_token_indexes(oToken)
    for iTemp in lTemp:
        if is_token_at_start_of_line(iTemp, oTokenMap):
            lReturn.append(iTemp)
    return lReturn


def filter_tokens_between_tokens(lTokens, oStart, oEnd, oTokenMap):
    lStart = oTokenMap.get_token_indexes(oStart)
    lEnd = oTokenMap.get_token_indexes(oEnd)

    lReturn = []
    for oToken in lTokens:
        for iStart, iEnd in zip(lStart, lEnd):
            lReturn.extend(oTokenMap.get_token_indexes_between_indexes(oToken, iStart, iEnd))
    return lReturn


def get_indexes_of_tokens_between(lStartToken, lEndTokens, oTokenMap):
    '''
    This function will take a list of start tokens and a list of end tokens.
    It will return a list of indexes of either a start token or an end token.
    A start token index will be returned if another start token was found before an end token.
    An end token index will be returned if the next token index is a start token.
    '''
    lReturn = []
    lStartIndexes = oTokenMap.get_token_indexes(lStartToken)
    lEndIndexes = get_indexes_of_token_list(lEndTokens, oTokenMap)

    for iStartIndex, iStart in enumerate(lStartIndexes):
        try:
            iNextStart = lStartIndexes[iStartIndex + 1]
        except IndexError:
            try:
                iNextStart = lEndIndexes[-1] + 1
            except IndexError:
                lReturn.append(iStartIndex)
                return lReturn
        iEndIndex = iStart
        for iEnd in lEndIndexes:
            if iEnd > iStart and iEnd < iNextStart:
                iEndIndex = iEnd
            if iEnd > iNextStart:
                break
        lReturn.append(iEndIndex)
    return lReturn
