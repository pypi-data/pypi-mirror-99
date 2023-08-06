'''
This module provides functions for rules to use.
'''


def get_violation_line_number(dViolation):
    '''
    Returns a line number of a violation.

    Parameters:

      dViolation: Violation dictionary

    Returns:  integer
    '''
    return dViolation.get_line_number()


def get_violation_at_line_number(lViolations, iLineNumber):
    '''
    Returns a violation from a violation dictionary at the given line number.

    Parameters:

      lViolation : (List of Violation dictionaries)

      iViolation : (integer)

    Return: Violation Dictionary
    '''
    for oViolation in lViolations:
        if oViolation.get_line_number() == iLineNumber:
            return oViolation


def get_violation_solution_at_line_number(lViolations, iLineNumber):
    '''
    Returns a the solution for a violation at a given line number.

    Parameters:

      lViolation : (List of Violation dictionaries)

      iViolation : (integer)

    Return: string
    '''
    try:
        dViolation = get_violation_at_line_number(lViolations, iLineNumber)
        return dViolation['solution']
    except TypeError:
        oViolation = get_violation_at_line_number(lViolations, iLineNumber)
        try:
            return oViolation.get_solution()
        except AttributeError:
            return None
