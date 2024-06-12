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

    def get_data_transformer_object(self, raw_data_path):
        try:
            # Load the datasets
            raw_dataset = pd.read_csv(raw_data_path)
            
            logging.info("Read of raw data completed")

            # Step 1: Distinguish Classes
            logging.info("Separating Grades")

            raw_dataset = raw_dataset.rename(columns={'Current Year (17/18)': 'Grade'})
            

            # Create columns of Exam
            feature_exam = [feature for feature in raw_dataset.columns if 'Math' in feature or 'Science' in feature or 'English' in feature]
            logging.info(f"Exam features: {feature_exam}")
            print(feature_exam)

            # Step 2: Create Dataset with required features
            new_data_feature = feature_exam + ['Grade']
            logging.info(f"New data features: {new_data_feature}")
            print(new_data_feature)

            raw_data = raw_dataset[new_data_feature]
            

            # Step 3: Group similar features
            feature_math = [feature for feature in raw_data.columns if 'Math' in feature]
            logging.info(f"Math features: {feature_math}")
            print(feature_math)

            feature_science = [feature for feature in raw_data.columns if 'Science' in feature]
            logging.info(f"Science features: {feature_science}")
            print(feature_science)

            feature_english = [feature for feature in raw_data.columns if 'English' in feature]
            logging.info(f"English features: {feature_english}")
            print(feature_english)

            logging.info("Grouing of similar features is completed")

            logging.info(f"Raw data shape before reshaping: {raw_data.shape}")
            

            # Convert to numeric data types
            raw_data = raw_data.apply(pd.to_numeric, errors='coerce')
        

            raw_data_reshaped = raw_data.values.reshape(-1, raw_data.shape[1])
            print(raw_data_reshaped)
            
            logging.info(f"Raw data reshaped shape: {raw_data_reshaped.shape}")
            logging.info(f"New data features: {new_data_feature}")

            # Save the reshaped data
            reshaped_raw_path = os.path.join('artifacts', 'raw_reshaped.csv')
            pd.DataFrame(raw_data_reshaped, columns=new_data_feature).to_csv(reshaped_raw_path, index=False)
            
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
                raw_data_reshaped,
                new_data_feature,
                raw_data
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_transformation = DataTransformation()
    raw_data_path = 'artifacts/data.csv'
    data_transformation.get_data_transformer_object(raw_data_path)
