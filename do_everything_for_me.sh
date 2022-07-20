#!/bin/bash
INFILE="${1:?You need to specify the input file (Nessus CSV)}"
OUTFILE="${2:?You need to specify the name (not the extension) of the output file}"
TEXTLANG="${3:-es}"
QUANTITY="${4:-0}"

PARSER="${PWD}/one_line_csv_parser.py"
FORMATTER="${PWD}/detailed_table_generator.py"
MISSING_SCRIPT=2

if [[ -f "${PARSER}" ]]; then
    if [[ ! -x "${PARSER}" ]]; then
        chmod +x "${PARSER}"
    fi
else
    echo -e "${PARSER} needed" >&2
    exit MISSING_SCRIPT
fi

if [[ -f "${FORMATTER}" ]]; then
    if [[ ! -x "${FORMATTER}" ]]; then
        chmod +x "${FORMATTER}"
    fi
else
    echo -e "${FORMATTER} needed" >&2
    exit MISSING_SCRIPT
fi

"${PARSER}" -l 'Risk' -L 'critical,high,medium', -o "${OUTFILE}".csv -n '\\' -q "${QUANTITY}" "${INFILE}"
"${FORMATTER}" -s "${OUTFILE}".csv -o "${OUTFILE}".tex -l "${TEXTLANG}"
