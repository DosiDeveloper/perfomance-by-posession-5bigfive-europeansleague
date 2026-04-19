from multiprocessing import Pool
import os

from gdown import download_folder as gdownload_folder
import pandas as pd

from src.config import config_default

dir_data = config_default.folder_data_state_path["Processed"]

def transform_csv_to_parquet(file):
    df = pd.read_csv(file)
    df.to_parquet(dir_data / f"{file.name[:-4]}.parquet", index=False)
    print("Transformed: ", file.name)
    os.remove(file)


if __name__ == "__main__":
    file = [file for file in dir_data.glob("*.csv") if file.is_file()]
    try:
        gdownload_folder(config_default.data_url, output=str(
        dir_data), quiet=False, use_cookies=False)
    except Exception as e:
        print(f"Error downloading data: {e}")
    with Pool() as pool:
        pool.map(transform_csv_to_parquet, file)
    

