import pytest
from pathlib import Path
import tempfile
import pandas as pd

from src.data_processing.utils import transform_csv_to_parquet, transform_parquet_to_csv


class TestTransformCsvToParquet:
    def test_creates_parquet_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = Path(tmpdir) / "input.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            csv_file.write_text("id,name\n1,test\n")
            transform_csv_to_parquet(csv_file, output_dir)

            assert (output_dir / "input.parquet").exists()

    def test_preserves_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = Path(tmpdir) / "data.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            csv_file.write_text("col1,col2\n10,20\n30,40\n")
            transform_csv_to_parquet(csv_file, output_dir)

            df = pd.read_parquet(output_dir / "data.parquet")
            assert len(df) == 2
            assert list(df["col1"]) == [10, 30]

    def test_output_file_name_matches_input_stem(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_file = Path(tmpdir) / "my_file.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            csv_file.write_text("x\n1\n")
            transform_csv_to_parquet(csv_file, output_dir)

            assert (output_dir / "my_file.parquet").exists()


class TestTransformParquetToCsv:
    def test_creates_csv_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_file = Path(tmpdir) / "input.parquet"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            pd.DataFrame({"a": [1]}).to_parquet(parquet_file, index=False)
            transform_parquet_to_csv(parquet_file, output_dir)

            assert (output_dir / "input.csv").exists()

    def test_preserves_data(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_file = Path(tmpdir) / "data.parquet"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]}).to_parquet(
                parquet_file, index=False)
            transform_parquet_to_csv(parquet_file, output_dir)

            df = pd.read_csv(output_dir / "data.csv")
            assert len(df) == 3
            assert list(df["x"]) == [1, 2, 3]

    def test_output_file_name_matches_input_stem(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_file = Path(tmpdir) / "my_file.parquet"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            pd.DataFrame({"x": [1]}).to_parquet(parquet_file, index=False)
            transform_parquet_to_csv(parquet_file, output_dir)

            assert (output_dir / "my_file.csv").exists()

