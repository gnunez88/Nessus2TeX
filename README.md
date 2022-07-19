# Nessus2TeX

This tool aims to convert Nessus scans results into LaTeX tables.

## Why this tool?

When you do a scan with Nessus, if you want to export the results into a CSV file, Nessus does not a good job
in exporting in this format. Or maybe was just me who found out spreadsheets could not interpret it correctly
because of the newlines added in some "long" fields, like the Synopsis and Description fields.

Nevertheless, this is just one part, of the job. The next one is to have this information placed in LaTeX tables,
which should not be that difficult. However I have found out I couldn't just split the fields with commas, since
there were some commas within some fields, namely, Synopsis and Description (again).

Good thing I love Regex and I figured out how to get the fields the intended way.

## Usage

To parse the Nessus CSV to a CSV (only one register for line):

```bash
./one_line_csv_parser.py nessus.csv -l 'Risk' -L 'critical,high,medium' -o output.csv -n '\\'
```

As you can tell, I also added a feature to filter by the criticality, focusing on the most risky vulnerabilities
and reducing the number of meaningless entries.

Once we have the CSV file parsed, we can now create the tables:

```bash
./detailed_table_generator.py -s output.csv -o output.tex -l en
```

The `output.tex` file will contain the tables of the vulnerabilities, with its headings in the language specified
(available languages: English, Spanish and Catalan), and auto incrementing labels.

## This is too much to type

Yep, you are right, lazy bastard...

Here you are:

```bash
./do_everything_for_me.sh nessus.csv output
```

You can also specify the language (one of the available ones) with

```bash
./do_everything_for_me.sh nessus.csv output en
```

## Extra

Since I have faced some limitations with the memory LaTeX uses when working with loads of tables,
I decided to add another script, namely `this_is_cheating.sh` which takes a number of entries, by 
default 50, of vulnerabilities with criticality critical, high and medium.

