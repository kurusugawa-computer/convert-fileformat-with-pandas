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
$ convpandas csv2xlsx in.csv out.xlsx
```


```
Options:
  --sep TEXT                   Delimiter to use when reading csv.  [default:,]
  --encoding TEXT              Encoding to use when reading csv. List of Python standard encodings .  [default: utf-8]
  --quotechar TEXT             The character used to denote the start and end of a quoted item when reading csv.
  --string_to_numeric BOOLEAN  If true, convert string to numeric. [default: utf-8]
```

## xlsx2csv
Convert xlsx file to csv file.

```
$ convpandas xlsx2csv in.xlsx out.csv
```


```
Options:
  --sheet_name TEXT  Sheet name when reading xlsx. If not specified, read 1st sheet.
  --sep TEXT         Field delimiter for the output file.  [default: ,]
  --encoding TEXT    A string representing the encoding to use in the output file.  [default: utf-8]
  --quotechar TEXT   Character used to quote fields.
```
