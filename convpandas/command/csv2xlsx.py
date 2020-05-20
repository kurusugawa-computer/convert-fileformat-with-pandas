from pathlib import Path
from typing import Optional

import click
import openpyxl
import pandas


def _read_csv(
    csv_file: str, sep: str, encoding: str, quotechar: Optional[str],
) -> pandas.DataFrame:
    read_csv_kwargs = {
        "sep": sep,
        "encoding": encoding,
        "header": None,
    }
    if quotechar is not None:
        read_csv_kwargs.update({"quotechar": quotechar})
    return pandas.read_csv(csv_file, **read_csv_kwargs)


def _to_excel(
    df: pandas.DataFrame, xlsx_file: str, string_to_numeric: bool = True,
) -> None:
    Path(xlsx_file).parent.mkdir(exist_ok=True, parents=True)
    if string_to_numeric:
        convert_func = lambda e: pandas.to_numeric(e, errors="ignore")
    else:
        convert_func = lambda e: e

    workbook = openpyxl.Workbook(write_only=True)
    worksheet = workbook.create_sheet()
    for row_index, row in df.iterrows():
        worksheet.append([convert_func(value) for value in row])
    workbook.save(xlsx_file)


@click.command(name="csv2xlsx", help="Convert csv file to xlsx file.")
@click.argument("csv_file")
@click.argument("xlsx_file")
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
    help="If true, convert string to numeric. [default: utf-8]",
)
def csv2xlsx(
    csv_file: str,
    xlsx_file: str,
    sep: str,
    encoding: str,
    quotechar: Optional[str],
    string_to_numeric: bool,
):
    df = _read_csv(csv_file, sep=sep, encoding=encoding, quotechar=quotechar,)
    _to_excel(df=df, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
