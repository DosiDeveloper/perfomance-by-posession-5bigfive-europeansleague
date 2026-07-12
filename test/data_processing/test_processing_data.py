import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd
import tempfile

from src.data_processing.data_processor import DataProcessor
from src.data_processing.utils import transform_csv_to_parquet, transform_parquet_to_csv

class TestDataProcessor:
    @patch('src.data_processing.data_processor.gdownload_folder')
    def test_init_creates_processor_instance(self, mock_download):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path_state = {
                "Raw": Path(tmpdir) / "Raw",
                "Processed": Path(tmpdir) / "Processed"
            }
            data_path_state["Raw"].mkdir(parents=True)
            data_path_state["Processed"].mkdir(parents=True)
            
            (data_path_state["Raw"] / "test.csv").write_text("a,b\n1,2\n")
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "test_id"
                
                processor = DataProcessor(data_path=tmpdir, data_path_state=data_path_state)
            
            mock_download.assert_called_once()
            assert processor.data_path == tmpdir

    @patch('src.data_processing.data_processor.gdownload_folder')
    def test_download_data_success(self, mock_download):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path_state = {"Raw": Path(tmpdir)}
            config_mock = MagicMock()
            config_mock.data_folder_id = "test_id"
            config_mock.folder_data_state_path = data_path_state
            
            with patch('src.data_processing.data_processor.config_default', config_mock):
                processor = DataProcessor.__new__(DataProcessor)
                processor.data_path = tmpdir
                processor.data_path_state = data_path_state
                processor.download_data()
            
            mock_download.assert_called_once_with(
                "test_id", 
                output=str(Path(tmpdir)), 
                quiet=False, 
                use_cookies=False
            )

    @patch('src.data_processing.data_processor.gdownload_folder')
    @patch('src.data_processing.data_processor.Pool')
    def test_optimize_storage(self, mock_pool_class, mock_download):
        mock_pool = MagicMock()
        mock_pool_class.return_value = mock_pool
        
        with tempfile.TemporaryDirectory() as tmpdir:
            raw_dir = Path(tmpdir) / "Raw"
            raw_dir.mkdir()
            (raw_dir / "test.csv").write_text("a,b\n1,2\n")
            
            data_path_state = {
                "Raw": raw_dir,
                "Processed": Path(tmpdir) / "Processed"
            }
            data_path_state["Processed"].mkdir()
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "test_id"
                
                processor = DataProcessor.__new__(DataProcessor)
                processor.data_path = tmpdir
                processor.data_path_state = data_path_state
                processor.optimize_storage()
            
            mock_pool.__enter__.assert_called_once()


class TestTransformFunctions:
    def test_transform_csv_to_parquet(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "test.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()
            
            csv_path.write_text("name,value\ntest,100\n")
            transform_csv_to_parquet(csv_path, output_dir)
            
            parquet_file = output_dir / "test.parquet"
            assert parquet_file.exists()
            
            df = pd.read_parquet(parquet_file)
            assert len(df) == 1
            assert df.iloc[0]["name"] == "test"
            assert df.iloc[0]["value"] == 100

    def test_transform_csv_to_parquet_multiple_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "test.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()
            
            csv_path.write_text("id,name\n1,alice\n2,bob\n3,charlie\n")
            transform_csv_to_parquet(csv_path, output_dir)
            
            df = pd.read_parquet(output_dir / "test.parquet")
            assert len(df) == 3
            assert list(df["name"]) == ["alice", "bob", "charlie"]

    def test_transform_parquet_to_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_path = Path(tmpdir) / "test.parquet"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()
            
            df_orig = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
            df_orig.to_parquet(parquet_path, index=False)
            
            transform_parquet_to_csv(parquet_path, output_dir)
            
            csv_file = output_dir / "test.csv"
            assert csv_file.exists()
            
            df_result = pd.read_csv(csv_file)
            assert len(df_result) == 2
            assert list(df_result["a"]) == [1, 2]

    def test_transform_handles_empty_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "empty.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()
            
            csv_path.write_text("col1,col2\n")
            transform_csv_to_parquet(csv_path, output_dir)
            
            df = pd.read_parquet(output_dir / "empty.parquet")
            assert len(df) == 0
            assert list(df.columns) == ["col1", "col2"]

    def test_transform_handles_numeric_types(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "nums.csv"
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()
            
            csv_path.write_text("int_col,float_col\n42,3.14\n100,2.71\n")
            transform_csv_to_parquet(csv_path, output_dir)
            
            df = pd.read_parquet(output_dir / "nums.parquet")
            assert df["int_col"].dtype in [int, "int64"]
            assert df["int_col"].iloc[0] == 42
            assert df["float_col"].iloc[0] == 3.14
