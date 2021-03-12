import io
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union

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
    df_tuple_list: List[Tuple[str, pandas.DataFrame]],
    xlsx_file: str,
    string_to_numeric: bool = True,
) -> None:
    Path(xlsx_file).parent.mkdir(exist_ok=True, parents=True)
    if string_to_numeric:
        convert_func = _to_numeric
    else:
        convert_func = _do_not_anything

    workbook = openpyxl.Workbook(write_only=True)
    for sheet_name, df in df_tuple_list:
        if sheet_name == "-":
            worksheet = workbook.create_sheet()
        else:
            # sheet名は最大31文字にする必要がある
            if len(sheet_name) >= 32:
                sheet_name = sheet_name[:31]
            worksheet = workbook.create_sheet(title=sheet_name)
        values = df.values
        for row_index in range(df.shape[0]):
            row = values[row_index]
            worksheet.append([convert_func(value) for value in row])
    workbook.save(xlsx_file)


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
    if csv_file == tuple("-"):
        str_stdin = click.get_text_stream("stdin", encoding=encoding).read()
        df = _read_csv(
            io.StringIO(str_stdin), sep=sep, encoding=encoding, quotechar=quotechar
        )
        _to_excel([("-", df)], xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
        return

    if len(csv_file) == 0:
        print("Error: Specify 'CSV_FILE'.", file=sys.stderr)
        sys.exit(1)

    df_tuple_list = []
    for file in csv_file:
        file_path = Path(file)
        if not file_path.exists():
            print(f"No such file: '{file}'", file=sys.stderr)
            sys.exit(1)

        df = _read_csv(file, sep=sep, encoding=encoding, quotechar=quotechar)
        df_tuple_list.append((file_path.stem, df))

    _to_excel(df_tuple_list, xlsx_file=xlsx_file, string_to_numeric=string_to_numeric)
