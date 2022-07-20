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

If the amount of entries retrieved are quite high, using `pdflatex` will crash, since it does not have enough 
memory, for this reason I have implemented a flag on `one_line_csv_parser.py` to limit the number of results,
returning them by descending order of criticity (with the value of the CVSS v3.0 column).

Take into account some vulnerabilities might not have anything in this field but they have a CVSS v2 assigned.

### What Nessus fields I need

The Nessus fields needed are the following:
- CVE
- Risk
- Host
- Protocol
- Port
- Name
- Synopsis
- Description
- Solution
- Exploitable With
- CVSS v3.0 Base Score

The field *Synopsis* is not being used yet, but I decided to leave it to add a functionality with this
in the future.

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

You can also specify the amount of entries to get, it will return the most critical ones.
Here, it is retrieving the 250 most critical ones.

```bash
./do_everything_for_me.sh nessus.csv output en 250
```

# TODO

Take into account the other CVSS scores (2.0 and 2.1).
