import argparse


class PrettyHelpFormatter(
    argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    def _format_action(self, action: argparse.Action) -> str:
        return super()._format_action(action) + "\n"
