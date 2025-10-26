import os
import zipfile
import gdown
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self)-> str:
        '''
        Fetch data from the url
        '''
        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from : {dataset_url} into : {zip_download_dir}")

            file_id = dataset_url.split('/')[-2]
            prefix = "https://drive.google.com/uc?export=download&id="
            gdown.download(prefix + file_id, zip_download_dir)

            logger.info(f"Download data from {dataset_url} into : {zip_download_dir} is completed.")
        
        except Exception as e:
            raise e
    
    def extract_zip_file(self)->None:
        '''
        Extract zip file into the unzip directory
        '''
        try:
            unzip_dir = self.config.unzip_dir
            zip_file_path = self.config.local_data_file

            logger.info(f"Extracting data from : {zip_file_path} to : {unzip_dir}")

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
            
            logger.info(f"Extraction completed successfully.")

        except Exception as e:
            raise e