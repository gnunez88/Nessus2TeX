#!/usr/bin/env python3

# Values

## Conflicting characters
conflicting_characters = [
        ['{', '+++left-brace+++'],      # Saving the left brace symbol
        ['}', '+++right-brace+++'],     # Saving the right brace symbol
        ['\\\\', '+++newline+++'],      # Saving the newline symbol
        ['\\', '\\textbackslash{}'],
        ['_', '\\_'],
        ['&', '\&'],
        ['%', '\%'],
        ['$', '\$'],
        ['~', '\\textasciitilde{}'],
        ['^', '\\textasciicircum{}'],
        ['+++left-brace+++', '\{'],     # Converting back the left brace symbol
        ['+++right-brace+++', '\}'],    # Converting back the right brace symbol
        ['+++newline+++', '\\\\']       # Converting back the newline symbol
    ]

# Functions

def resolve_conflicts(text:str) -> str:
    '''Changes conflicting LaTeX characters to maintain their original meaning.

    Parameters
    ----------
    text : str
        Text target to have conflicting characters switched.

    Returns
    -------
    str
        Text with conflicting characters switched for safer ones.
    '''
    for conflicting_character in conflicting_characters:
        text = text.replace(conflicting_character[0], conflicting_character[1])
    return text
