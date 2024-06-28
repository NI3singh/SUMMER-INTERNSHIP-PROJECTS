import sys  # Import sys for system-specific parameters and functions
import os  # Import os for operating system dependent functionality
from dataclasses import dataclass  # Import dataclass for configuration handling

import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation

from src.exception import CustomException  # Import custom exception handler
from src.logger import logging  # Import logging module for logging messages
from src.utils import save_object  # Import utility function to save objects

# DataTransformationConfig dataclass to hold configuration options
@dataclass
class DataTransformationConfig:
    transformed_obj_file_path: str = os.path.join('artifacts', "transformed_data.pkl")  # Default path for saving transformation object

# DataTransformation class for transforming raw data
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()  # Initialize with default configuration

    # Method to perform data transformation
    def get_data_transformer_object(self, raw_data_path):
        try:
            # Load raw dataset from CSV
            dataset = pd.read_csv(raw_data_path)
            logging.info("Read of raw data completed")  # Log successful data read

            # Step 1: Distinguish Classes (assuming 'Current Year (17/18)' represents grades)
            logging.info("Separating Grades")
            dataset = dataset.rename(columns={'Current Year (17/18)': 'Grade'})  # Rename column to 'Grade' for clarity

            # Step 2: Identify Exam-related features
            feature_exam = [feature for feature in dataset.columns if 'Math' in feature or 'Science' in feature or 'English' in feature]
            logging.info(f"Exam features: {feature_exam}")  # Log identified exam-related features

            raw_data = dataset[feature_exam]  # Select only exam-related features

            # Step 3: Group similar features (assuming 'Math', 'Science', 'English' are distinct subjects)
            feature_math = [feature for feature in raw_data.columns if 'Math' in feature]
            logging.info(f"Math features: {feature_math}")  # Log math-related features

            feature_science = [feature for feature in raw_data.columns if 'Science' in feature]
            logging.info(f"Science features: {feature_science}")  # Log science-related features

            feature_english = [feature for feature in raw_data.columns if 'English' in feature]
            logging.info(f"English features: {feature_english}")  # Log english-related features

            logging.info("Grouping of similar features is completed")  # Log completion of feature grouping

            logging.info(f"Raw data shape before reshaping: {raw_data.shape}")  # Log shape of raw data before reshaping

            # Convert all data to numeric types
            raw_data = raw_data.apply(pd.to_numeric, errors='coerce')

            # Reshape data into a 2-dimensional array suitable for further processing
            raw_data_reshaped = raw_data.values.reshape(-1, raw_data.shape[1])
            logging.info(f"Raw data reshaped shape: {raw_data_reshaped.shape}")  # Log shape of reshaped data
            logging.info(f"New Exam feature: {feature_exam}")  # Log list of exam-related features

            # Save reshaped data to CSV file
            reshaped_raw_path = os.path.join('artifacts', 'raw_reshaped.csv')
            pd.DataFrame(raw_data_reshaped, columns=feature_exam).to_csv(reshaped_raw_path, index=False)
            logging.info("Data transformation completed.")  # Log completion of data transformation

            # Prepare transformation object for saving
            transformation = {
                'feature_math': feature_math,
                'feature_science': feature_science,
                'feature_english': feature_english,
            }

            # Save transformation object to file
            save_object(
                file_path=self.data_transformation_config.transformed_obj_file_path,
                obj=transformation
            )
            logging.info(f"Transformation object saved at: {self.data_transformation_config.transformed_obj_file_path}")  # Log path where transformation object is saved

            return (
                raw_data_reshaped,
                feature_exam,
                feature_math,
                feature_science,
                feature_english,
            )

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs

# Entry point of the script
if __name__ == "__main__":
    data_transformation = DataTransformation()  # Create instance of DataTransformation class
    raw_data_path = 'artifacts/raw_data.csv'  # Specify path to raw data CSV file
    data_transformation.get_data_transformer_object(raw_data_path)  # Initiate data transformation process
