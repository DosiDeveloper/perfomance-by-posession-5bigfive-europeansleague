import os
from pathlib import Path

import duckdb
from loguru import logger


class Config:
    def __init__(self):
        self.data_folder_id = os.getenv("DATA_ID", "1F_xPO4nGhPlZ5yqTMCXVpQ7KiENuO8bv")
        self.folder_data_path = Path(
            os.getenv("FOLDER_DATA_PATH", Path(__file__).parent.parent / "data")
        )
        # Pipeline
        self.folder_data_state_path = {
            "bronze": self.folder_data_path / "bronze",
            "silver": self.folder_data_path / "silver",
            "gold": self.folder_data_path / "gold",
        }
        self.oltp_db_path = Path(
            os.getenv("OLTP_DB_PATH", f"{self.folder_data_path}/db.sqlite3")
        )
        self.olap_db_path = Path(os.getenv("OLAP_DB_PATH", f"{self.folder_data_path}/duck.db"))

    def setup(self):
        self.create_folders()
        self.create_db_files()

    def create_db_files(self):
        if not self.olap_db_path.exists():
            conn = duckdb.connect(self.olap_db_path)
            conn.sql("")
            conn.close()
            logger.info("Olap db file has created successfully")
        logger.info("Olap db file already exists")
        if not self.oltp_db_path.exists():
            self.oltp_db_path.touch()
            logger.info("Oltp db file has created successfully")
        logger.info("Oltp db file already exists")

    def create_folders(self):
        if not self.folder_data_path.exists():
            self.folder_data_path.mkdir(parents=True, exist_ok=True)
        for folder in self.folder_data_state_path.values():
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
        logger.info("Data folder has been created sucessfully")


config_default = Config()
