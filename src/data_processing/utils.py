from pathlib import Path
from loguru import logger

import pandas as pd
from src.config import config_default


def transform_csv_to_parquet(file: Path, folder_output):
    df = pd.read_csv(file)
    df.to_parquet(folder_output /
                  f"{file.stem}.parquet", index=False)
    logger.info(f"Transformed: {file.name}")


def transform_parquet_to_csv(file: Path, folder_output):
    df = pd.read_parquet(file)
    df.to_csv(folder_output /
                  f"{file.stem}.csv", index=False)
    logger.info(f"Transformed: {file.name}")
