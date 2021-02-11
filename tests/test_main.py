import os
from pathlib import Path

from click.testing import CliRunner

from convpandas.command.csv2xlsx import csv2xlsx
from convpandas.command.xlsx2csv import xlsx2csv

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

out_path = Path("./tests/out/")
out_path.mkdir(exist_ok=True, parents=True)

data_path = Path("./tests/data")


class Test_csv2xlsx:
    runner = CliRunner()

    def test_standard(self):
        result = self.runner.invoke(
            csv2xlsx, [str(data_path / "test.csv"), str(out_path / "out.xlsx")]
        )
        assert result.exit_code == 0

    def test_convert_stdin_csv(self):
        result = self.runner.invoke(
            csv2xlsx, ["-", str(out_path / "out2.xlsx")], input="name,id\nAlice,1\n"
        )
        assert result.exit_code == 0

    def test_convert_multiple_csv_to_xlsx(self):
        result = self.runner.invoke(
            csv2xlsx,
            [
                str(data_path / "test.csv"),
                str(data_path / "test2.csv"),
                str(data_path / "test.csv"),
                str(out_path / "out3.xlsx"),
            ],
        )
        assert result.exit_code == 0


class Test_xlsx2csv:
    runner = CliRunner()

    def test_standard(self):
        result = self.runner.invoke(
            xlsx2csv, [str(data_path / "test.xlsx"), str(out_path / "out.csv")]
        )
        assert result.exit_code == 0

    def test_specify_sheetname(self):
        result = self.runner.invoke(
            xlsx2csv,
            [
                str(data_path / "test.xlsx"),
                str(out_path / "out2.csv"),
                "--sheet_name",
                "bob",
            ],
        )
        assert result.exit_code == 0

    def test_output_stdout_csv(self):
        result = self.runner.invoke(xlsx2csv, [str(data_path / "test2.xlsx"), "-"])
        assert result.exit_code == 0
        assert result.output == "name,age\n田中,23\n"
