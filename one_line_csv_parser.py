#!/usr/bin/python3

import argparse
import pdb
import re
import signal
import sys

from tools.array_tools import append_field_idx

# Global variables
outfile = None
newline = '\\n'

def close():
    global outfile
    if outfile is not None:
        outfile.close()


def stop(sig, frame):
    sys.write.stderr('\n[!] Exiting...\n')
    close()
    sys.exit(1)


def pos_int(user_input:str) -> int:
    '''Checks if the input is a positive integer or the number zero (0).

    Parameters
    ----------
    user_input : str
        A string which should result in a valid positive integer or the number
        zero (0).

    Returns
    -------
    int
        A positive integer or zero, derived from the input string.
    '''
    pattern = r'^\+*\d+$'
    integer = re.match(pattern, user_input)
    if integer is None:
        error_message = f'{user_input} is not a valid number (positive integer)'
        raise argparse.ArgumentError(error_message)
    else:
        integer = int(integer.group().lstrip('+'))
    return integer


def main(args):
    signal.signal(signal.SIGINT, stop)  # Triggered with Ctrl+C

    if args.debug:
        pdb.set_trace()

    # TODO: convert args into a dictionary (arguments)

    # Variables
    fields = list()
    entries = list()
    global newline
    newline = args.newline
    quantity = args.quantity
    level_header = args.level_header
    levels = ["all"] if "all".lower() in list(map(str.lower, args.levels.split(','))) else args.levels.split(',')
    infile = args.infile
    global outfile
    if args.outfile:
        outfile = args.outfile

    with open(infile, 'r') as f:
        lines = f.read().split('\n')
        headers = lines[0]
        lines = lines[1:-1]  # The first line is the header, the last line is empty

    # Parsing the multiline entries
    entry = ''
    for line in lines:
        entry += line
        if entry[-1] == '"':
            entries.append(entry)
            entry = ''
        else:
            entry += newline

    # Filtering results
    results = list()
    if 'all' in levels:
        for entry in entries:
            results.append(entry)
    else:
        level_index = headers.split(',').index(level_header)
        for entry in entries:
            for level in levels:
                # Checking if the criticality matches
                if level.lower() == entry.split(',')[level_index].strip('"').lower():
                    results.append(entry)
                    break  # Only one criticality match is needed

    # Limiting the number of results
    if quantity != 0:
        auxiliar_idx = headers.split(',').index('CVSS v3.0 Base Score')
        auxiliar_list = append_field_idx(results,
                                         auxiliar_idx,
                                         delimiter=',')
        # Sorting the list by the second field (index 1)
        auxiliar_list.sort(key=lambda x: x[1])
        # Extracting the first field
        results = [x[0] for x in auxiliar_list if x[1] != '']
        # Since list.sort() reverse in ascending order, we can have the most
        # critical first by reversing the list
        results.reverse()
        # Getting the first "quantity" entries (most critical)
        results = results[0:quantity+1]

    # Inserting the headers at the beginning
    results.insert(0, headers)


    # Output
    csv = '\n'.join(results)
    #if arguments['outfile']:
    if outfile:
        with open(outfile, 'w') as f:
            f.write(csv)
    else:
        print(csv, end='')


# Standalone
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str, help="Input file")
    parser.add_argument('-o', '--outfile', type=str, help="Output file")
    parser.add_argument('-l', '--level-header', type=str, help="Level header (criticality)", default='Risk')
    parser.add_argument('-L', '--levels', type=str, help="Levels to filter, separated by comma (default: all)", default="all")
    parser.add_argument('-n', '--newline', type=str, help="Newline character", default='\\n')
    parser.add_argument('-q', '--quantity', type=pos_int, help="Number of entries taken by decreasing criticality, 0 means no limit (default: 0)", default=0)
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="Debug mode")
    args = parser.parse_args()
    main(args)
