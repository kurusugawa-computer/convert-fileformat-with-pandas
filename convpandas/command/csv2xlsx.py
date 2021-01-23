import os
import sys
from pathlib import Path
from typing import Optional

import click
import openpyxl
import pandas


def _read_csv(
    csv_file: str,
    sep: str,
    encoding: str,
    quotechar: Optional[str],
) -> pandas.DataFrame:
    read_csv_kwargs = {
        "sep": sep,
        "encoding": encoding,
        "header": None,
    }
    if quotechar is not None:
        read_csv_kwargs.update({"quotechar": quotechar})
    return pandas.read_csv(csv_file, **read_csv_kwargs)


def _to_numeric(value):
    return pandas.to_numeric(value, errors="ignore")


def _do_not_anything(value):
    return value


def _to_excel(
    df: pandas.DataFrame,
    xlsx_file: str,
    string_to_numeric: bool = True,
) -> None:
    Path(xlsx_file).parent.mkdir(exist_ok=True, parents=True)
    if string_to_numeric:
        convert_func = _to_numeric
    else:
        convert_func = _do_not_anything

    workbook = openpyxl.Workbook(write_only=True)
    worksheet = workbook.create_sheet()
    for row_index, row in df.iterrows():
        worksheet.append([convert_func(value) for value in row])
    workbook.save(xlsx_file)


@click.command(name="csv2xlsx", help="Convert csv file to xlsx file.")
@click.argument("csv_file")
@click.argument("xlsx_file", required=False)
@click.option(
    "--sep", default=",", show_default=True, help="Delimiter to use when reading csv."
)
@click.option(
    "--encoding",
    default="utf-8",
    show_default=True,
    help="Encoding to use when reading csv. List of Python standard encodings .",
)
@click.option(
    "--quotechar",
    help="The character used to denote the start and end of a quoted item when reading csv.",
)
@click.option(
    "--string_to_numeric",
    type=bool,
    default=True,
    help="If true, convert string to numeric. [default: true]",
)
def csv2xlsx(
    csv_file: str,
    xlsx_file: Optional[str],
    sep: str,
    encoding: str,
    quotechar: Optional[str],
    string_to_numeric: bool,
):
    if not os.path.exists(csv_file):
        print(f"No such file or directory: '{csv_file}'", file=sys.stderr)
        sys.exit(1)

    df = _read_csv(csv_file, sep=sep, encoding=encoding, quotechar=quotechar)
    if xlsx_file is None:
        csv_file_path = Path(csv_file)
        xlsx_file_name = f"{csv_file_path.stem}.xlsx"
        xlsx_file = str(csv_file_path.parent / xlsx_file_name)

    _to_excel(df=df, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
