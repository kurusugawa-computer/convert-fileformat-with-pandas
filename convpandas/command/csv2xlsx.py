import click


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
    "--read_csv_args",
    help="Indicates 'pandas.read_csv' arguments with JSON-formatted. See also https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html .",
)
@click.option(
    "--to_excel_args",
    help="Indicates 'pandas.DataFrame.to_excel' arguments with JSON-formatted. See also https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html .",
)
def csv2xlsx(
    csv_file,
    xlsx_file,
    sep: str,
    encoding: str,
    quotechar: str,
    read_csv_args,
    to_excel_args,
):
    pass
