import io
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

import click
import openpyxl
import pandas


def _read_csv(
    csv_file: Union[str, io.TextIOBase],
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


@click.command(name="csv2xlsx", help="Convert csv file to xlsx file.")
@click.argument("csv_file", nargs=-1)
@click.argument("xlsx_file", nargs=1)
@click.option(
    "--sep", default=",", show_default=True, help="Delimiter to use when reading csv."
)
@click.option(
    "--encoding",
    default="utf-8",
    show_default=True,
    help="Encoding to use when reading csv. List of Python standard encodings. "
    "(https://docs.python.org/3/library/codecs.html#standard-encodings)",
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
    csv_file: Tuple[str],
    xlsx_file: str,
    sep: str,
    encoding: str,
    quotechar: Optional[str],
    string_to_numeric: bool,
):
    df_dict = {}

    if csv_file == tuple("-"):
        str_stdin = click.get_text_stream("stdin", encoding=encoding).read()
        df = _read_csv(
            io.StringIO(str_stdin), sep=sep, encoding=encoding, quotechar=quotechar
        )
        df_dict["-"] = df
        _to_excel(df_dict, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
        return

    for file in csv_file:
        file_path = Path(file)
        if not file_path.exists():
            print(f"No such file: '{file}'", file=sys.stderr)
            sys.exit(1)

        df = _read_csv(file, sep=sep, encoding=encoding, quotechar=quotechar)
        append_df_to_dict(df_dict, sheet_name=file_path.stem, df=df)

    _to_excel(df_dict, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
