import click

import convpandas
from convpandas.command.csv2xlsx import csv2xlsx
from convpandas.command.xlsx2csv import xlsx2csv


@click.group()
@click.version_option(version=convpandas.__version__)
def cli():
    pass


cli.add_command(csv2xlsx)
cli.add_command(xlsx2csv)

if __name__ == "__main__":
    cli()
