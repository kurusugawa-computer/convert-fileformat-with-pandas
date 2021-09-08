import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import pandas

from convpandas.common.cli import PrettyHelpFormatter


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


def xlsx2csv(
    xlsx_file: str,
    csv_file: str,
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


def main(args):
    xlsx2csv(
        xlsx_file=args.xlsx_file,
        csv_file=args.csv_file,
        sheet_name=args.sheet_name,
        sep=args.sep,
        encoding=args.encoding,
        quotechar=args.quotechar,
    )


def add_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser(
        "xlsx2csv",
        help="Convert xlsx file to csv file.",
        formatter_class=PrettyHelpFormatter,
    )
    parser.set_defaults(command_help=parser.print_help)

    parser.add_argument("xlsx_file", type=str)
    parser.add_argument("csv_file", type=str)

    parser.add_argument(
        "--sheet_name",
        type=str,
        help="Sheet name when reading xlsx. If not specified, read 1st sheet.",
    )

    parser.add_argument(
        "--sep", default=",", help="Field delimiter for the output file."
    )

    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="A string representing the encoding to use in the output file.",
    )
    parser.add_argument(
        "--quotechar",
        default='"',
        help="Character used to quote fields.",
    )

    parser.set_defaults(subcommand_func=main)
    return parser
