import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    transformed_obj_file_path: str = os.path.join('artifacts', "transformed_data.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self, train_data_path, test_data_path):
        try:
            # Load the datasets
            train_dataset = pd.read_csv(train_data_path)
            test_dataset = pd.read_csv(test_data_path)
            logging.info("Read the train and test data completed")

            # Step 1: Distinguish Classes
            logging.info("Separating Grades")
            train_dataset = train_dataset.rename(columns={'Current Year (17/18)': 'Grade'})
            test_dataset = test_dataset.rename(columns={'Current Year (17/18)': 'Grade'})

            # Create columns of Exam
            feature_exam = [feature for feature in train_dataset.columns if 'Math' in feature or 'Science' in feature or 'English' in feature]
            logging.info(f"Exam features: {feature_exam}")
            print(feature_exam)

            # Step 2: Create Dataset with required features
            new_data_feature = feature_exam + ['Grade']
            logging.info(f"New data features: {new_data_feature}")
            print(new_data_feature)

            train_data = train_dataset[new_data_feature]
            test_data = test_dataset[new_data_feature]

            # Step 3: Group similar features
            feature_math = [feature for feature in train_data.columns if 'Math' in feature]
            logging.info(f"Math features: {feature_math}")
            print(feature_math)

            feature_science = [feature for feature in train_data.columns if 'Science' in feature]
            logging.info(f"Science features: {feature_science}")
            print(feature_science)

            feature_english = [feature for feature in train_data.columns if 'English' in feature]
            logging.info(f"English features: {feature_english}")
            print(feature_english)

            logging.info(f"Train data shape before reshaping: {train_data.shape}")
            logging.info(f"Test data shape before reshaping: {test_data.shape}")

            # Convert to numeric data types
            train_data = train_data.apply(pd.to_numeric, errors='coerce')
            test_data = test_data.apply(pd.to_numeric, errors='coerce')

            train_data_reshaped = train_data.values.reshape(-1, train_data.shape[1])
            test_data_reshaped = test_data.values.reshape(-1, test_data.shape[1])

            logging.info(f"Train data reshaped shape: {train_data_reshaped.shape}")
            logging.info(f"Test data reshaped shape: {test_data_reshaped.shape}")
            logging.info(f"New data features: {new_data_feature}")

            # Save the reshaped data
            reshaped_train_path = os.path.join('artifacts', 'train_reshaped.csv')
            reshaped_test_path = os.path.join('artifacts', 'test_reshaped.csv')
            pd.DataFrame(train_data_reshaped, columns=new_data_feature).to_csv(reshaped_train_path, index=False)
            pd.DataFrame(test_data_reshaped, columns=new_data_feature).to_csv(reshaped_test_path, index=False)

            logging.info("Data transformation completed.")

            # Save the transformation object
            transformation = {
                'feature_math': feature_math,
                'feature_science': feature_science,
                'feature_english': feature_english,
            }

            save_object(
                file_path=self.data_transformation_config.transformed_obj_file_path,
                obj=transformation
            )
            logging.info(f"Transformation object saved at: {self.data_transformation_config.transformed_obj_file_path}")

            return (
                train_data_reshaped,
                test_data_reshaped,
                new_data_feature
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_transformation = DataTransformation()
    train_data_path = 'artifacts/train.csv'
    test_data_path = 'artifacts/test.csv'
    data_transformation.get_data_transformer_object(train_data_path, test_data_path)
