#!/usr/bin/env python3

from tools.csv_tools import csv_parser

# Functions

def append_field_idx(array:list, field_pos:int, delimiter=',') -> list:
    '''Extracts a field from a unparsed structured list

    Parameters
    ----------
    array : list
        Target list to act on.
    field_pos : int
        Field position to extract from the list to append later.
    delimiter : str
        Field separator (default: ',').

    Returns
    -------
    list
        2D list with the original values and the target value extracted.
    '''
    result = list()
    for entry in array:
        field_value = csv_parser(entry, delimiter=delimiter)[field_pos]
        result.append([entry, field_value])

    return result


def append_field_name(array:list, field_name:str, delimiter=',') -> list:
    '''Extracts a field from a unparsed structured list

    Parameters
    ----------
    array : list
        Target list to act on.
    field_name : str
        Field name to extract from the list to append later, it must exist.
    delimiter : str
        Field separator (default: ',').

    Returns
    -------
    list
        2D list with the original values and the target value extracted.
    '''
    result = list()
    for entry in array:
        field_value = csv_parser(entry, delimiter=delimiter).index(field_name)
        result.append([entry, field_value])

    return result

