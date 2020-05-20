import json

import click


@click.command(name="xlsx2csv", help="Convert xlsx file to csv file.")
@click.argument("xlsx_file")
@click.argument("csv_file")
@click.option(
    "--sheet_name",
    help="Sheet name when reading xlsx. If not specified, read 1st sheet.",
)
@click.option(
    "--sep", default=",", show_default=True, help="Delimiter to use when writing csv."
)
@click.option(
    "--encoding",
    default="utf-8",
    show_default=True,
    help="Encoding to use when writing csv. List of Python standard encodings .",
)
@click.option(
    "--quotechar",
    help="The character used to denote the start and end of a quoted item when writing csv.",
)
@click.option(
    "--read_excel_args",
    help="Indicates 'pandas.read_excel' arguments with JSON-formatted. This option has the highest priority. See also https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html .",
)
@click.option(
    "--to_csv_args",
    help="Indicates 'pandas.DataFrame.to_csv' arguments with JSON-formatted. This option has the highest priority. See also https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html .",
)
def xlsx2csv(
    xlsx_file: str,
    csv_file: str,
    sheet_name: str,
    sep: str,
    encoding: str,
    quotechar: str,
    read_excel_args,
    to_csv_args,
):
    read_excel_kwargs
    if read_excel_args is not None:
        read_excel_kwargs = json.loads(read_excel_args)
    if to_csv_args is not None:
        to_csv_kwargs = json.loads(to_csv_args)
