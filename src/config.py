import os
from pathlib import Path


class Config:
    def __init__(self):
        self.data_url = os.getenv(
            'DATA_URL', 'https://drive.google.com/drive/folders/1F_xPO4nGhPlZ5yqTMCXVpQ7KiENuO8bv?usp=sharing')
        self.folder_data_path = os.getenv(
            'FOLDER_DATA_PATH', str(Path(__file__).parent.parent / "Data"))
        self.folder_data_state_path = {
            "Clean": Path(self.folder_data_path) / "Clean",
            "Processed": Path(self.folder_data_path) / "Processed",
        }
        self.db_path = os.getenv(
            'DB_PATH', f'{self.folder_data_path}/db.sqlite3')

        # visualization
        self.dash_pages = Path(__file__).parent / "dashboard" / "pages"
        self.create_folders()

    def create_folders(self):
        if not Path(self.folder_data_path).exists():
            Path(self.folder_data_path).mkdir(parents=True, exist_ok=True)
        for folder in self.folder_data_state_path.values():
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)


config_default = Config()
