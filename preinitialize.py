from dotenv import load_dotenv

from src.config import config_default
from src.data_processing.data_processor import data_processor
# from src.data_processing.data_processor import data_processor


load_dotenv()
config_default.setup()
data_processor.run_pipeline(config_default.oltp_db_path, config_default.olap_db_path)

# data_processor.download_data()
