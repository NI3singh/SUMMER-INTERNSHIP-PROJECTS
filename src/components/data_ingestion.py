import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components import data_preparation
from src.components import data_transformation
from src.components import model_trainer


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
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

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            dataset.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train Test Split Initiated")

            train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the Data is Completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    from src.components.model_trainer import ModelTrainer

    data_preparation_obj = data_preparation.DataPreparation()
    numerical_features, categorical_features = data_preparation_obj.initiate_data_preparation(train_data_path, test_data_path)

    data_transformation_obj = data_transformation.DataTransformation()
    train_data_reshaped, test_data_reshaped, new_data_feature = data_transformation_obj.get_data_transformer_object('artifacts/train.csv', 'artifacts/test.csv')
    model_trainer_obj = ModelTrainer()
    model_trainer_obj.initiate_model_training(train_data_reshaped, test_data_reshaped, new_data_feature)
