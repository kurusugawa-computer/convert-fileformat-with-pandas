import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import click
import pandas


def _read_excel(xlsx_file: str, sheet_name: Optional[str]) -> pandas.DataFrame:
    read_excel_kwargs: Dict[str, Any] = {"header": None}
    if sheet_name is not None:
        read_excel_kwargs.update({"sheet_name": sheet_name})
    return pandas.read_excel(xlsx_file, **read_excel_kwargs)


def _to_csv(
    df: pandas.DataFrame,
    filepath_or_buffer: Any,
    sep: str,
    encoding: str,
    quotechar: str,
) -> None:
    if isinstance(filepath_or_buffer, str):
        Path(filepath_or_buffer).parent.mkdir(exist_ok=True, parents=True)

    to_csv_kwargs = {
        "sep": sep,
        "encoding": encoding,
        "quotechar": quotechar,
        "header": False,
        "index": False,
    }
    df.to_csv(filepath_or_buffer, **to_csv_kwargs)


@click.command(name="xlsx2csv", help="Convert xlsx file to csv file.")
@click.argument("xlsx_file")
@click.argument("csv_file")
@click.option(
    "--sheet_name",
    help="Sheet name when reading xlsx. If not specified, read 1st sheet.",
)
@click.option(
    "--sep", default=",", show_default=True, help="Field delimiter for the output file."
)
@click.option(
    "--encoding",
    default="utf-8",
    show_default=True,
    help="A string representing the encoding to use in the output file.",
)
@click.option(
    "--quotechar",
    default='"',
    help="Character used to quote fields.",
)
def xlsx2csv(
    xlsx_file: str,
    csv_file: Optional[str],
    sheet_name: Optional[str],
    sep: str,
    encoding: str,
    quotechar: str,
):
    if not os.path.exists(xlsx_file):
        print(f"No such file or directory: '{xlsx_file}'", file=sys.stderr)
        sys.exit(1)

    df = _read_excel(xlsx_file, sheet_name=sheet_name)

    filepath_or_buffer: Any = csv_file
    if csv_file == "-":
        filepath_or_buffer = sys.stdout

    _to_csv(df, filepath_or_buffer, sep=sep, encoding=encoding, quotechar=quotechar)
