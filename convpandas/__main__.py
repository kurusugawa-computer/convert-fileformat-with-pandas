import argparse
from typing import Optional, Sequence

import convpandas
from convpandas.command.csv2xlsx import add_parser as csv2xlsx_add_parser
from convpandas.command.xlsx2csv import add_parser as xlsx2csv_add_parser
from convpandas.common.cli import PrettyHelpFormatter


def cli(arguments: Optional[Sequence[str]] = None):
    """
    注意： `deprecated`なツールは、サブコマンド化しない。

    Args:
        arguments: コマンドライン引数。テストコード用

    """

    parser = argparse.ArgumentParser(
        description="Command Line Interface for AnnoFab",
        formatter_class=PrettyHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"convpandas {convpandas.__version__}"
    )
    parser.set_defaults(command_help=parser.print_help)

    subparsers = parser.add_subparsers(dest="command_name")
    csv2xlsx_add_parser(subparsers)
    xlsx2csv_add_parser(subparsers)

    if arguments is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(arguments)

    if hasattr(args, "subcommand_func"):
        args.subcommand_func(args)

    else:
        # 未知のサブコマンドの場合はヘルプを表示
        args.command_help()


if __name__ == "__main__":
    cli()
