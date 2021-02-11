# convert-fileformat-with-pandas
Convert file format with [pandas](https://pandas.pydata.org/).

[![Build Status](https://travis-ci.org/yuji38kwmt/convpandas.svg?branch=master)](https://travis-ci.org/yuji38kwmt/convpandas)
[![PyPI version](https://badge.fury.io/py/convpandas.svg)](https://badge.fury.io/py/convpandas)
[![Python Versions](https://img.shields.io/pypi/pyversions/convpandas.svg)](https://pypi.org/project/convpandas/)

# Requirements
* Python 3.7+

# Install

```
$ pip install convpandas
```

https://pypi.org/project/convpandas/


# Usage

## csv2xlsx
Convert csv file to xlsx file.

```
$ convpandas csv2xlsx --help
Usage: convpandas csv2xlsx [OPTIONS] [CSV_FILE]... XLSX_FILE

  Convert csv file to xlsx file.

Options:
  --sep TEXT                   Delimiter to use when reading csv.  [default:,]

  --encoding TEXT              Encoding to use when reading csv. List of Python standard encodings. (https://docs.python.org/3/library/codecs.html#standard-encodings) [default: utf-8]

  --quotechar TEXT             The character used to denote the start and end of a quoted item when reading csv.

  --string_to_numeric BOOLEAN  If true, convert string to numeric. [default:true]
```


Convert `in.csv` to `out.xlsx` .

```
$ convpandas csv2xlsx in.csv out.xlsx
```


When specifying `-` for `CSV_FILE`, get from STDIN. 

```
$ convpandas csv2xlsx - out.xlsx < in.csv
```

Convert `in1.csv` and `in2.csv` to `out.xlsx` . Sheet name is csv filename without its suffix.  

```
$ convpandas csv2xlsx in1.csv in2.csv out.xlsx
```

![](/home/vagrant/Documents/convert-fileformat-with-pandas/docs/img/output_xlsx_file_from_multiple_csv.png)


## xlsx2csv
Convert xlsx file to csv file.

```
$ convpandas xlsx2csv --help
Usage: convpandas xlsx2csv [OPTIONS] XLSX_FILE CSV_FILE

  Convert xlsx file to csv file.

Options:
  --sheet_name TEXT  Sheet name when reading xlsx. If not specified, read 1st sheet.

  --sep TEXT         Field delimiter for the output file.  [default: ,]

  --encoding TEXT    A string representing the encoding to use in the output file.  [default: utf-8]

  --quotechar TEXT   Character used to quote fields. 

  --help             Show this message and exit.
```


Convert `in.xlsx` to `out.csv` .

```
$ convpandas csv2xlsx in.xlsx out.csv
```


When specifying `-` for `CSV_FILE`, write to STDOUT. 

```
$ convpandas csv2xlsx in.xlsx -
name,age
Alice,23
```

With specifying `--sheet_name`, you can select sheet name that you want to convert.

```
$ convpandas csv2xlsx in.xlsx out.csv --sheet_name sheet2
```
