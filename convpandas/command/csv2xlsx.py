import argparse
import io
import sys
from pathlib import Path
from typing import Dict, List, Union

import click
import openpyxl
import pandas

from convpandas.common.cli import PrettyHelpFormatter


def _read_csv(
    csv_file: Union[str, io.TextIOBase],
    sep: str,
    encoding: str,
    quotechar: str,
) -> pandas.DataFrame:
    read_csv_kwargs = {
        "sep": sep,
        "encoding": encoding,
        "quotechar": quotechar,
        "header": None,
    }
    return pandas.read_csv(csv_file, **read_csv_kwargs)


def _to_numeric(value):
    return pandas.to_numeric(value, errors="ignore")


def _do_not_anything(value):
    return value


def _to_excel(
    df_dict: Dict[str, pandas.DataFrame],
    xlsx_file: str,
    string_to_numeric: bool = True,
) -> None:
    Path(xlsx_file).parent.mkdir(exist_ok=True, parents=True)
    if string_to_numeric:
        convert_func = _to_numeric
    else:
        convert_func = _do_not_anything

    workbook = openpyxl.Workbook(write_only=True)
    for sheet_name, df in df_dict.items():
        if sheet_name == "-":
            worksheet = workbook.create_sheet()
        else:
            worksheet = workbook.create_sheet(title=sheet_name)
        values = df.values
        for row_index in range(df.shape[0]):
            row = values[row_index]
            worksheet.append([convert_func(value) for value in row])
    workbook.save(xlsx_file)


def append_df_to_dict(
    df_dict: Dict[str, pandas.DataFrame], sheet_name: str, df: pandas.DataFrame
):
    if sheet_name not in df_dict:
        df_dict[sheet_name] = df
        return

    index = 1
    while True:
        new_sheet_name = f"{sheet_name}_{index}"
        if new_sheet_name not in df_dict:
            df_dict[new_sheet_name] = df
            return df_dict
        index += 1


def csv2xlsx(
    csv_files: List[str],
    xlsx_file: str,
    *,
    sep: str,
    encoding: str,
    quotechar: str,
    string_to_numeric: bool,
    sheet_names: List[str],
):
    if sheet_names is not None:
        if len(sheet_names) != len(csv_files):
            print(
                "Size of csv_files and size of sheet_name do not match.",
                file=sys.stderr,
            )
            sys.exit(1)

    df_dict: Dict[str, pandas.DataFrame] = {}

    if len(csv_files) == 1 and csv_files[0] == "-":
        str_stdin = click.get_text_stream("stdin", encoding=encoding).read()
        df = _read_csv(
            io.StringIO(str_stdin), sep=sep, encoding=encoding, quotechar=quotechar
        )
        if sheet_names is None:
            df_dict["-"] = df
        else:
            df_dict[sheet_names[0]] = df
        _to_excel(df_dict, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
        return

    if sheet_names is None:
        for file in csv_files:
            file_path = Path(file)
            if not file_path.exists():
                print(f"No such file: '{file}'", file=sys.stderr)
                sys.exit(1)

            df = _read_csv(file, sep=sep, encoding=encoding, quotechar=quotechar)
            append_df_to_dict(df_dict, sheet_name=file_path.stem, df=df)
    else:
        for file, name in zip(csv_files, sheet_names):
            file_path = Path(file)
            if not file_path.exists():
                print(f"No such file: '{file}'", file=sys.stderr)
                sys.exit(1)

            df = _read_csv(file, sep=sep, encoding=encoding, quotechar=quotechar)
            append_df_to_dict(df_dict, sheet_name=name, df=df)

    _to_excel(df_dict, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)


def main(args):
    csv2xlsx(
        csv_files=args.csv_files,
        xlsx_file=args.xlsx_file,
        sep=args.sep,
        encoding=args.encoding,
        quotechar=args.quotechar,
        string_to_numeric=args.string_to_numeric,
        sheet_names=args.sheet_name,
    )


def add_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser(
        "csv2xlsx",
        help="Convert csv file to xlsx file.",
        formatter_class=PrettyHelpFormatter,
    )
    parser.set_defaults(command_help=parser.print_help)

    parser.add_argument("csv_files", type=str, nargs="+")
    parser.add_argument("xlsx_file", type=str)

    parser.add_argument("--sep", default=",", help="Delimiter to use when reading csv.")

    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding to use when reading csv. List of Python standard encodings.\n"
        "https://docs.python.org/3/library/codecs.html#standard-encodings",
    )
    parser.add_argument(
        "--quotechar",
        default='"',
        help="The character used to denote the start and end of a quoted item when reading csv.",
    )

    parser.add_argument(
        "--string_to_numeric",
        action="store_true",
        help="If specified, convert string to numeric.",
    )

    parser.add_argument("--sheet_name", type=str, nargs="+")

    parser.set_defaults(subcommand_func=main)
    return parser
