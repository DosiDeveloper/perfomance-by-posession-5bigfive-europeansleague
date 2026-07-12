import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import tempfile

from src.data_processing.data_processor import DataProcessor


class TestDriveFolderConnection:
    @patch('src.data_processing.data_processor.gdownload_folder')
    def test_download_folder_calls_gdown(self, mock_download):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path_state = {"Raw": Path(tmpdir)}
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "test_folder_123"
                
                DataProcessor(data_path=tmpdir, data_path_state=data_path_state)
            
            mock_download.assert_called_once_with(
                "test_folder_123",
                output=str(Path(tmpdir)),
                quiet=False,
                use_cookies=False
            )

    @patch('src.data_processing.data_processor.gdownload_folder')
    def test_download_uses_config_id(self, mock_download):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path_state = {"Raw": Path(tmpdir)}
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "custom_folder_id"
                
                DataProcessor(data_path=tmpdir, data_path_state=data_path_state)
            
            call_args = mock_download.call_args
            assert call_args[0][0] == "custom_folder_id"

    @patch('src.data_processing.data_processor.gdownload_folder')
    @patch('src.data_processing.data_processor.Pool')
    def test_download_writes_to_raw_folder(self, mock_pool, mock_download):
        mock_pool.return_value.__enter__.return_value = MagicMock()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            raw_dir = Path(tmpdir) / "Raw"
            raw_dir.mkdir()
            
            data_path_state = {
                "Raw": raw_dir,
                "Processed": Path(tmpdir) / "Processed"
            }
            data_path_state["Processed"].mkdir()
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "test_id"
                
                DataProcessor(data_path=tmpdir, data_path_state=data_path_state)
            
            args, kwargs = mock_download.call_args
            assert str(raw_dir) == kwargs["output"]


class TestDriveConnectionErrorHandling:
    @patch('src.data_processing.data_processor.gdownload_folder')
    def test_download_failure_logs_error(self, mock_download):
        mock_download.side_effect = Exception("Network error")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path_state = {"Raw": Path(tmpdir)}
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "test_id"
                mock_config.data_folder_id = "bad_id"
                
                with patch('logging.error') as mock_log:
                    try:
                        DataProcessor(data_path=tmpdir, data_path_state=data_path_state)
                    except:
                        pass
                    
                    mock_log.assert_called()

    @patch('src.data_processing.data_processor.gdownload_folder')
    def test_download_continues_on_error(self, mock_download):
        mock_download.side_effect = Exception("Download failed")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            raw_dir = Path(tmpdir) / "Raw"
            raw_dir.mkdir()
            (raw_dir / "test.csv").write_text("a\n1\n")
            
            data_path_state = {
                "Raw": raw_dir,
                "Processed": Path(tmpdir) / "Processed"
            }
            data_path_state["Processed"].mkdir()
            
            with patch('src.data_processing.data_processor.config_default') as mock_config:
                mock_config.folder_data_path = tmpdir
                mock_config.folder_data_state_path = data_path_state
                mock_config.data_folder_id = "bad_id"
                
                processor = DataProcessor(data_path=tmpdir, data_path_state=data_path_state)
            
            assert mock_download.called
