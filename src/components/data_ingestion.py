import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from dataclasses import dataclass
from src.components import data_preparation
from src.components import data_transformation



@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data Ingestion Method")
        try:
            df = pd.read_csv(r'notebook/data/StudentDataset.csv')
            dataset = df.copy()
            logging.info("Successfully Read the Dataset as Dataframe")

            dataset['Id'] = [i for i in range(len(dataset))]
            dataset.set_index('Id', inplace=True)

            logging.info("indexing of ID column is completed")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            dataset.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Ingestion of the Data is Completed")
            
            return (
                self.ingestion_config.raw_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    raw_data_path = obj.initiate_data_ingestion()

    from src.components.model_trainer import ModelTrainer

    data_preparation_obj = data_preparation.DataPreparation()
    numerical_features, categorical_features = data_preparation_obj.initiate_data_preparation(raw_data_path='artifacts/data.csv')

    data_transformation_obj = data_transformation.DataTransformation()
    raw_data_reshaped,new_data_feature,raw_data = data_transformation_obj.get_data_transformer_object(raw_data_path='artifacts/data.csv')

    model_trainer_obj = ModelTrainer()
    train_data_reshaped, test_data_reshaped = model_trainer_obj.split_data(raw_data_reshaped, new_data_feature)
    model_trainer_obj.initiate_model_training(new_data_feature, train_data_reshaped, test_data_reshaped)