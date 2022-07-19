#!/bin/bash
CSV_FILE="${1:?Input CSV large file}"
SAMPLE_LINES="${2:-50}"

INFILE="${CSV_FILE}".csv
OUTFILE="${CSV_FILE}".csv

OUTPUT=""
OUTPUT+="$(head -1 ${INFILE})"
#OUTPUT+="$(awk -F, '$2="\"Critical\""' ${INFILE} | head -n ${SAMPLE_LINES})"
#OUTPUT+="$(awk -F, '$2="\"High\""' ${INFILE} | head -n ${SAMPLE_LINES})"
#OUTPUT+="$(awk -F, '$2="\"Medium\""' ${INFILE} | head -n ${SAMPLE_LINES})"
OUTPUT+="$(grep -i '"Critical"' ${INFILE} | head -n ${SAMPLE_LINES})"
OUTPUT+="$(grep -i '"High"' ${INFILE} | head -n ${SAMPLE_LINES})"
OUTPUT+="$(grep -i '"Medium"' ${INFILE} | head -n ${SAMPLE_LINES})"

cp "${CSV_FILE}".csv "${CSV_FILE}".csv.bak
echo "${OUTPUT}" > "${OUTFILE}"
