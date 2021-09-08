import io
import os
import sys
from pathlib import Path

from convpandas.__main__ import cli

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

out_path = Path("./tests/out/")
out_path.mkdir(exist_ok=True, parents=True)

data_path = Path("./tests/data")


class Test_csv2xlsx:
    def test_standard(self):
        cli(["csv2xlsx", str(data_path / "test.csv"), str(out_path / "out.xlsx")])

    def test_convert_stdin_csv(self):
        sys.stdin = io.StringIO("name,id\nAlice,1\n")
        cli(["csv2xlsx", "-", str(out_path / "out2.xlsx")])

    def test_convert_multiple_csv_to_xlsx(self):
        cli(
            [
                "csv2xlsx",
                str(data_path / "test.csv"),
                str(data_path / "test2.csv"),
                str(data_path / "test.csv"),
                str(out_path / "out3.xlsx"),
            ]
        )

    def test_convert_multiple_csv_to_xlsx_with_sheetnames(self):
        cli(
            [
                "csv2xlsx",
                str(data_path / "test.csv"),
                str(data_path / "test2.csv"),
                str(data_path / "test.csv"),
                str(out_path / "out3.xlsx"),
                "--sheet_name",
                "alice bob",
                "bob",
                "chris",
            ]
        )


class Test_xlsx2csv:
    def test_standard(self):
        cli(["xlsx2csv", str(data_path / "test.xlsx"), str(out_path / "out.csv")])

    def test_specify_sheetname(self):
        cli(
            [
                "xlsx2csv",
                str(data_path / "test.xlsx"),
                str(out_path / "out2.csv"),
                "--sheet_name",
                "bob",
            ]
        )

    def test_output_stdout_csv(self, capsys):
        cli(["xlsx2csv", str(data_path / "test2.xlsx"), "-"])

        captured = capsys.readouterr()
        assert captured.out == "name,age\n田中,23\n"
