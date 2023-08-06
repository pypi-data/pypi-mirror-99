
lSingleCharacterSymbols = [',', ':', '(', ')', '\'', '"', '+', '&', '-', '*', '/', '<', '>', ';', '=', '[', ']', '?']
lTwoCharacterSymbols = ['=>','**', ':=', '/=', '>=', '<=', '<>', '??', '?=', '?<', '?>', '<<', '>>', '--']
lThreeCharacterSymbols = ['?/=', '?<', '?<=', '?>=']


def create(sString):
    '''
    This function takes a string and returns a list of tokens.
    '''
    lCharacters = []

    for sChar in sString:
        lCharacters.append(sChar)

    lCharacters = combine_whitespace(lCharacters)
    lCharacters = combine_two_character_symbols(lCharacters)
    lCharacters = combine_characters_into_words(lCharacters)
    lCharacters = combine_string_literals(lCharacters)
    lCharacters = combine_character_literals(lCharacters)
    lCharacters = combine_comments(lCharacters)

    return lCharacters


def combine_comments(lChars):
    lReturn = []
    sComment = ''
    bComment = False
    for sChar in lChars:
        if sChar.startswith('--') and not bComment:
            sComment += sChar
            bComment = True
            continue
        if not bComment:
            lReturn.append(sChar)
        else:
            sComment += sChar

    if bComment:
        lReturn.append(sComment)

    return lReturn


def combine_string_literals(lChars):
    lReturn = []
    sLiteral = ''
    bLiteral = False
    for sChar in lChars:
        if sChar == '"' and not bLiteral:
            sLiteral += sChar
            bLiteral = True
            continue
        if not bLiteral:
            lReturn.append(sChar)
        else:
            sLiteral += sChar
        if sChar == '"' and bLiteral:
            bLiteral = False
            lReturn.append(sLiteral)
            sLiteral = ''

    return lReturn


def combine_character_literals(lChars):
    lReturn = []
    sLiteral = ''
    bLiteral = False
    for iChar, sChar in enumerate(lChars):
        try:
            if sChar == "'" and lChars[iChar + 2] == "'" and len(lChars[iChar + 1]) == 1 and not bLiteral:
                sLiteral += sChar
                bLiteral = True
                continue
        except IndexError:
            pass
        if not bLiteral:
            lReturn.append(sChar)
        else:
            sLiteral += sChar
        if sChar == "'" and bLiteral:
            bLiteral = False
            lReturn.append(sLiteral)
            sLiteral = ''

    return lReturn


def combine_characters_into_words(lChars):
    lReturn = []
    sTemp = ''
    for sChar in lChars:
        if len(sChar) > 1:
            if sTemp != '':
                lReturn.append(sTemp)
            lReturn.append(sChar)
            sTemp = ''
        elif sChar == ' ':
            if sTemp != '':
                lReturn.append(sTemp)
            lReturn.append(sChar)
            sTemp = ''
        elif sChar in lSingleCharacterSymbols:
            if sTemp != '':
                lReturn.append(sTemp)
            lReturn.append(sChar)
            sTemp = ''
        else:
            sTemp += sChar

    if len(sTemp) != 0:
        lReturn.append(sTemp)

    return lReturn


def combine_whitespace(lChars):
    lReturn = []
    sSpace = ''
    for sChar in lChars:
        if sChar == ' ':
            sSpace += sChar
        else:
            if sSpace != '':
                lReturn.append(sSpace)
                sSpace = ''
            lReturn.append(sChar)

    if sSpace != '':
        lReturn.append(sSpace)

    return lReturn


def combine_two_character_symbols(lChars):
    lReturn = []
    sNextChar = ''
    bSkip = False
    for iChar, sChar in enumerate(lChars):
        if bSkip:
            bSkip = False
            continue
        try:
            sNextChar = lChars[iChar + 1]
        except IndexError:
            sNextChar = ''
        if sChar + sNextChar in lTwoCharacterSymbols:
            bSkip = True
            lReturn.append(sChar + sNextChar)
        else:
            lReturn.append(sChar)
    return lReturn
