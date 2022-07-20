#!/usr/bin/python3

import argparse
import pdb
import re
import signal
import sys

from tools.csv_tools import csv_parser
from tools.tex_tools import resolve_conflicts

# Global variables
outfile = None      # Output file
verbosity = 0       # 

## Colours
critical_colour = 'FE0000'
high_colour = 'FD6864'
medium_colour = 'F56B00'
white = 'FFFFFF'

## Texts
computer_info_text = {
        'en': "Computer information",
        'es': "Información del equipo",
        'ca': "Informació de l'ordinador"
    }

vuln_text = {
        'en': "Vulnerabilities",
        'es': "Vulnerabilidades",
        'ca': "Vulnerabilitats"
    }

description_text = {
        'en': "Description",
        'es': "Descripción",
        'ca': "Descripció"
    }

criticality_text = {
        'en': "Criticality",
        'es': "Criticidad",
        'ca': "Criticitat"
    }

criticality_critical_text = {
        'en': "Critical",
        'es': "Crítica",
        'ca': "Crítica"
    }

criticality_high_text = {
        'en': "High",
        'es': "Alta",
        'ca': "Alta"
    }

criticality_medium_text = {
        'en': "Medium",
        'es': "Media",
        'ca': "Mitja"
    }

criticality_low_text = {
        'en': "Low",
        'es': "Baja",
        'ca': "Baixa"
    }

criticality_none_text = {
        'en': "None",
        'es': "Ninguna",
        'ca': "Cap"
    }

criticality_command = {
        'critical': "\\Critica",
        'high': "\\Alta",
        'medium': "\\Media",
        'low': "\\Baja",
        'none': "\\Ninguna"
    }

recommendation_text = {
        'en': "Recommendations",
        'es': "Recomendaciones",
        'ca': "Recomendacions"
    }

## Structures
doc_structure_begin = '''
\\documentclass[{classfile}]{{subfiles}}
\\begin{{document}}

'''

doc_structure_end = r'''
\end{document}
'''

doc_structure_begin_summary = r'''
%% Vulnerabilities summary
'''

doc_structure_begin_details = r'''
%% Vulnerabilities' details
'''

summary_table = '''
\\begin{{table}}[H]\\label{{tbl:summary}}
    \\centering
    \\begin{{tabular}}{{|c|c|c|c|c|}}
    \\cline{{1-1}} \\cline{{3-3}} \\cline{{5-5}}
    \\cellcolor[HTML]{{{critical_colour}}}{{\\color[HTML]{{{white}}} \\textbf{{{critical_values}({critical_values_with_exploit})}}}} &
    &
    \\cellcolor[HTML]{{{high_colour}}}{{\\color[HTML]{{{white}}} \\textbf{{{high_values}({high_values_with_exploit})}}}} &
    &
    \\cellcolor[HTML]{{{medium_colour}}}{{\\color[HTML]{{{white}}} \\textbf{{{medium_values}({medium_values_with_exploit})}}}} 
    \\\\ \\cline{{1-1}} \\cline{{3-3}} \\cline{{5-5}}
    {criticality_critical_text} & &
    {criticality_high_text} & &
    {criticality_medium_text}
    \\\\ \\cline{{1-1}} \\cline{{3-3}} \\cline{{5-5}}
    \\end{{tabular}}
\\end{{table}}
'''

summary_table_values = {
        "critical": 0,
        "critical_with_exploit": 0,
        "high": 0,
        "high_with_exploit": 0,
        "medium": 0,
        "medium_with_exploit": 0
    }

detailed_table = '''
\\begin{{table}}[H]
\\begin{{tabular}}{{|ll|}}
    \\hline
    \\rowcolor[HTML]{{34CDF9}}
    \\multicolumn{{2}}{{|l|}}{{\\cellcolor[HTML]{{34CDF9}}\\textbf{{{computer_info_text}}}}} \\\\ \\hline
    % IP
    IP
    & {host}
    \\\\ \\hline
    % Port
    PORT
    & {port}
    \\\\ \\hline
    \\rowcolor[HTML]{{34CDF9}}
    \\multicolumn{{2}}{{|l|}}{{\\cellcolor[HTML]{{34CDF9}}\\textbf{{{vuln_text}}}}} \\\\ \\hline
    \\multicolumn{{2}}{{|l|}}{{
        \\begin{{tabular}}[c]{{p{{15cm}}}}
            % Vulnerability
            {vuln}
        \\end{{tabular}}
    }} \\\\ \\hline
    \\rowcolor[HTML]{{34CDF9}}
    \\multicolumn{{2}}{{|l|}}{{\\cellcolor[HTML]{{34CDF9}}\\textbf{{{description_text}}}}} \\\\ \\hline
    \\multicolumn{{2}}{{|l|}}{{
        \\begin{{tabular}}[c]{{p{{15cm}}}}
            % Description
            {description}
        \\end{{tabular}}
    }} \\\\ \\hline
    \\rowcolor[HTML]{{34CDF9}}
    \\multicolumn{{2}}{{|l|}}{{\\cellcolor[HTML]{{34CDF9}}\\textbf{{{criticality_text}}}}} \\\\ \\hline
    \\multicolumn{{2}}{{|l|}}{{
        % Criticality
        {criticality}
    }} \\\\ \\hline
    \\rowcolor[HTML]{{34CDF9}}
    \\multicolumn{{2}}{{|l|}}{{\\cellcolor[HTML]{{34CDF9}}\\textbf{{{recommendation_text}}}}} \\\\ \\hline
    \\multicolumn{{2}}{{|l|}}{{
        \\begin{{tabular}}[c]{{p{{15cm}}}}
            % Recommendation
            {recommendation}
        \\end{{tabular}}
    }} \\\\ \\hline
\\end{{tabular}}
\\caption{{
    % Reference
    {reference}
}}\\label{{tbl:{label}}}
\\end{{table}}
'''


# Functions

def close():
    global outfile
    if outfile is not None:
        if verbosity > 0:
            print("Closing file...")
        outfile.close()
        

def stop(sig, frame):
    sys.stderr.write('\n[!] Exiting...\n')
    close()
    sys.exit(1)


def main(args):
    signal.signal(signal.SIGINT, stop)

    if args.debug:
        pdb.set_trace()

    # Variables
    global summary_table_values
    lang = args.language
    classfile = args.classfile
    if args.outfile:
        global outfile
        outfile = args.outfile
    with open(args.sourcefile, 'r') as f:
        sourcefile = f.read().split('\n')
        # Removing last line if empty
        if sourcefile[-1] == '':
            sourcefile.pop()
        # Separating the header from the actual data
        headers = sourcefile[0]
        sourcefile = sourcefile[1:]

    # Get indeces
    indeces = {
            "cve": headers.split(',').index('CVE'),
            "criticality": headers.split(',').index('Risk'),
            "host": headers.split(',').index('Host'),
            "protocol": headers.split(',').index('Protocol'),
            "port": headers.split(',').index('Port'),
            "vuln": headers.split(',').index('Name'),
            "synopsis": headers.split(',').index('Synopsis'),
            "description": headers.split(',').index('Description'),
            "solution": headers.split(',').index('Solution'),
            "cvss_v3": headers.split(',').index('CVSS v3.0 Base Score'),
            "exploit": headers.split(',').index('Metasploit')
        }

    # Detailed tables
    label_count = 0
    detailed_tables = list()
    for vuln_entry in sourcefile:
        label_count += 1
        # Parsing CSV format
        fields = csv_parser(vuln_entry, delimiter=',')
        # Assigning values to variables within detailed_table
        host = fields[indeces["host"]]
        port = fields[indeces["port"]]
        protocol = fields[indeces["protocol"]]
        vuln = fields[indeces["vuln"]]
        description = fields[indeces["description"]]
        criticality = fields[indeces["criticality"]]
        recommendation = fields[indeces["solution"]]
        reference = f'{label_count:04d}'
        label = f'vuln_{label_count:04d}'
        public_exploit = fields[indeces["exploit"]]
        # Updating global values
        if criticality.lower() == "critical":
            summary_table_values['critical'] += 1
            if public_exploit.lower() == "true":
                summary_table_values['critical_with_exploit'] += 1
        elif criticality.lower() == "high":
            summary_table_values['high'] += 1
            if public_exploit.lower() == "true":
                summary_table_values['high_with_exploit'] += 1
        elif criticality.lower() == "medium":
            summary_table_values['medium'] += 1
            if public_exploit.lower() == "true":
                summary_table_values['medium_with_exploit'] += 1
        # Rendering the table
        rendered_detailed_table = detailed_table.format(
                computer_info_text = computer_info_text[lang],
                vuln_text = vuln_text[lang],
                description_text = description_text[lang],
                criticality_text = criticality_text[lang],
                recommendation_text = recommendation_text[lang],
                host = host,
                port = f'{port}/{protocol}',
                vuln = resolve_conflicts(vuln),
                description = resolve_conflicts(description),
                criticality = criticality_command[criticality.lower()],
                reference = resolve_conflicts(reference),
                recommendation = resolve_conflicts(recommendation),
                label = label
            )
        # Saving the rendered table
        detailed_tables.append(rendered_detailed_table)


    # Summary table
    rendered_summary_table = summary_table.format(
            critical_colour = critical_colour,
            high_colour = high_colour,
            medium_colour = medium_colour,
            white = white,
            critical_values = summary_table_values["critical"],
            high_values = summary_table_values["high"],
            medium_values = summary_table_values["medium"],
            critical_values_with_exploit = summary_table_values["critical_with_exploit"],
            high_values_with_exploit = summary_table_values["high_with_exploit"],
            medium_values_with_exploit = summary_table_values["medium_with_exploit"],
            criticality_critical_text = criticality_critical_text[lang],
            criticality_high_text = criticality_high_text[lang],
            criticality_medium_text = criticality_medium_text[lang]
        )

    # Document
    document  = ''
    document += doc_structure_begin.format(classfile=classfile)
    document += doc_structure_begin_summary
    document += rendered_summary_table
    document += doc_structure_begin_details
    document += '\n\n\n'.join(detailed_tables)
    document += doc_structure_end

    with open(outfile, 'w') as f:
        f.write(document)


# Standalone
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--classfile', type=str, help="Class file (default: ../report.tex)", default='../report.tex')
    parser.add_argument('-s', '--sourcefile', type=str, help="Source file (CSV) where to take the data from", required=True)
    parser.add_argument('-o', '--outfile', type=str, help="Output file (default: details.tex", default='details.tex')
    parser.add_argument('-l', '--language', type=str, help="Wording language (default: 'es')", choices=['en','es','ca'], default='es')
    parser.add_argument('-v', '--verbosity', action='count', default=0, help="Verbose mode")
    parser.add_argument('-d', '--debug', action='store_true', help="Debugging mode")
    args = parser.parse_args()
    main(args)
