from click.testing import CliRunner
import os
from pathlib import Path

from convpandas.command.csv2xlsx import csv2xlsx
from convpandas.command.xlsx2csv import xlsx2csv

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

out_path = Path("./tests/out/")
out_path.mkdir(exist_ok=True, parents=True)

data_path = Path("./tests/data")




def test_csv2xlsx():
    runner = CliRunner()
    result = runner.invoke(csv2xlsx,
                           [str(data_path/"test.csv"),
                                str(out_path/"out.xlsx")])
    assert result.exit_code == 0

def test_xlsx2csv():
    runner = CliRunner()
    result = runner.invoke(xlsx2csv,
                           [str(data_path/"test.xlsx"),
                                str(out_path/"out.csv")])
    assert result.exit_code == 0

