#!/usr/bin/python3

import argparse
import csv
import pdb
import re
import signal
import sys

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


def main(args):
    signal.signal(signal.SIGINT, stop)
    fields = list()
    entries = list()

    if args.debug:
        pdb.set_trace()

    # TODO: convert args into a dictionary (arguments)

    # Variables
    global newline
    newline = args.newline
    level_header = args.level_header
    #levels = args.levels.split(',') if args.levels else "all"
    levels = ["all"] if "all".lower() in list(map(str.lower, args.levels.split(','))) else args.levels.split(',')
    infile = args.infile
    global outfile
    if args.outfile:
        outfile = args.outfile

    #with open(arguments['infile'], 'r') as f:
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
                # Checking if the criticity matches
                if level.lower() == entry.split(',')[level_index].strip('"').lower():
                    results.append(entry)
                    break  # Only one criticity match is needed
    # Inserting the headers at the beginning
    results.insert(0, headers)


    # Output
    csv = '\n'.join(results)
    #if arguments['outfile']:
    if outfile:
        #with open(arguments['outfile'], 'w') as f:
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
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="Debug mode")
    args = parser.parse_args()
    main(args)
