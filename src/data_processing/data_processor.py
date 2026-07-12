import duckdb
from gdown import download  # type: ignore
from gdown import download_folder as gdownload_folder  # type: ignore
from loguru import logger

from src.config import config_default
from src.data_processing.transformations.bronze_layer import bronze_layer
from src.data_processing.utils import transform_csv_to_parquet


class DataProcessor:
    def __init__(
        self,
        data_path=config_default.folder_data_path,
        data_path_state=config_default.folder_data_state_path,
    ):
        self.data_path = data_path
        self.data_path_state = data_path_state

    def download_data(self):
        try:
            datalake_files = gdownload_folder(
                config_default.data_folder_id,
                use_cookies=False,
                skip_download=True,
                quiet=True,
            )
            for data_files in datalake_files:
                if data_files[1] not in list(
                    map(lambda f: f.name, self.data_path_state["Processed"].iterdir())
                ):
                    download(
                        id=data_files[0],
                        output=str(self.data_path_state["Processed"] / data_files[1]),
                        use_cookies=False,
                        quiet=True,
                    )
                    logger.info(f"File {data_files[1]} not found, downloading")
        except Exception as e:
            logger.error(f"Error downloading data: {e}")

    def optimize_storage(self):
        csv_files = list(self.data_path_state["Raw"].glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files for optimization.")

        for f in csv_files:
            transform_csv_to_parquet(f)

    def run_pipeline(self, oltp_db_path, olap_db_path):
        logger.info("Running pipeline")
        self.Pipeline(self.data_path_state, oltp_db_path, olap_db_path).run()

    class Pipeline:
        def __init__(self, folder_data_state_path, oltp_db_path, olap_db_path) -> None:
            self.folder_data_state_path = folder_data_state_path
            self.oltp_db_path = oltp_db_path
            self.olap_db_path = olap_db_path
            self._load_duckdb_extension()

        def run(self):
            with duckdb.connect(self.olap_db_path) as olap_conn:
                bronze_layer(olap_conn, self.oltp_db_path, self.folder_data_state_path["bronze"])

        def _load_duckdb_extension(self):
            with duckdb.connect() as conn:
                conn.execute("INSTALL sqlite; LOAD sqlite;")


data_processor = DataProcessor()
