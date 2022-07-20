#!/usr/bin/env python3

import re

def csv_parser(csv_file:str, delimiter=',') -> list:
    '''Parses a pseudo-CSV file into a CSV file

    Parameters
    ----------
    csv_file : str
        Pseudo-CSV file, a CSV file where a register can be multiline.
    delimiter : str
        The delimiter used in the Pseudo-CSV file (default: ',')

    Returns
    -------
    list
        List of the new CSV registers.
    '''
    pattern = r'(?<=")[^"]*?(?="(?:' + delimiter + r'"|$))'
    fields = re.findall(pattern, csv_file, re.MULTILINE)
    return fields


