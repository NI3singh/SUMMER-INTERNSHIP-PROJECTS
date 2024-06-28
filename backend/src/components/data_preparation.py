import pandas as pd  # Import pandas for data manipulation
import numpy as np  # Import numpy for numerical operations
from dataclasses import dataclass  # Import dataclass for configuration handling
import sys  # Import sys for system-specific parameters and functions
import os  # Import os for operating system dependent functionality
from src.exception import CustomException  # Import custom exception handler
from src.logger import logging  # Import logging module for logging messages
from src.utils import save_object  # Import utility function to save objects
from src.components import data_ingestion  # Import data ingestion component

# DataPreparationConfig dataclass to hold configuration options
@dataclass
class DataPreparationConfig:
    preparation_obj_file_path: str = os.path.join('artifacts', "preparation.pkl")  # Default path for saving preparation object

# DataPreparation class for preparing raw data
class DataPreparation:
    def __init__(self):
        self.data_preparation_config = DataPreparationConfig()  # Initialize with default configuration

    # Method to initiate data preparation
    def initiate_data_preparation(self, raw_data_path):
        try:
            # Load raw dataset from CSV
            dataset = pd.read_csv(raw_data_path)
            logging.info("Successfully Read the Raw data")  # Log successful data read

            # Step 1: Finding Missing Values
            features_na = [feature for feature in dataset.columns if dataset[feature].isnull().sum() > 1]
            logging.info(f"Features with missing values: {features_na}")  # Log features with missing values
            for feature in features_na:
                logging.info(f"{feature}: {np.round(dataset[feature].isnull().mean(), 4)}% missing values")  # Log percentage of missing values per feature

            # Step 2: Replace Missing Values with NaN
            def is_float(string):
                try:
                    float(string)
                    return True
                except ValueError:
                    return False

            feature_float = [feature for feature in dataset.columns if 'exam' in feature and dataset[feature].dtypes == 'O']
            logging.info(f"Float features: {feature_float}")  # Log float-type features
            for feature in feature_float:
                dataset[feature] = dataset[feature].apply(lambda x: x if is_float(x) else np.nan)  # Convert non-float values to NaN
                dataset[feature] = dataset[feature].astype(float)  # Convert column to float type

            logging.info("Successfully Completed Finding and Replacing of Missing Values")  # Log completion of missing values replacement

            # Step 3: Convert Datatype of Columns to Necessary Types
            for feature in feature_float:
                dataset[feature] = dataset[feature].astype(float)  # Convert float features to float type

            dataset.info()  # Display dataset information
            logging.info("Successfully Converted Datatypes of Columns to float")  # Log datatype conversion completion

            # Step 4: Distinguish Categorical and Numerical Features
            numerical_features = [feature for feature in dataset.columns if dataset[feature].dtypes != 'O']  # Identify numerical features
            logging.info(f"Numerical features: {numerical_features}")  # Log numerical features
            logging.info(dataset[numerical_features].head())  # Log sample of numerical feature data

            categorical_features = [feature for feature in dataset.columns if dataset[feature].dtypes == 'O']  # Identify categorical features
            logging.info(f"Categorical features: {categorical_features}")  # Log categorical features
            logging.info(dataset[categorical_features].head())  # Log sample of categorical feature data

            # Step 5: Replace NaN values in Numerical Features with Median Values
            numerical_with_nan = [feature for feature in dataset.columns if dataset[feature].isnull().sum() > 1 and dataset[feature].dtypes != 'O']
            logging.info(f"Numerical features with NaN: {numerical_with_nan}")  # Log numerical features with NaN
            for feature in numerical_with_nan:
                median_value = dataset[feature].median()  # Calculate median value of the feature
                dataset[feature] = dataset[feature].fillna(median_value)  # Replace NaN values with median
            logging.info(dataset[numerical_with_nan].isnull().sum())  # Log sum of NaN values after replacement

            logging.info("Data preparation completed.")  # Log completion of data preparation

            # Prepare dictionary object for saving
            preparation = {
                'numerical_features': numerical_features,
                'categorical_features': categorical_features,
            }

            # Save preparation object to file
            save_object(
                file_path=self.data_preparation_config.preparation_obj_file_path,
                obj=preparation
            )
            logging.info(f"Preparation object saved at: {self.data_preparation_config.preparation_obj_file_path}")  # Log path where preparation object is saved

            return (
                numerical_features,
                categorical_features,
            )

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs

# Entry point of the script
if __name__ == "__main__":
    data_preparation = DataPreparation()  # Create instance of DataPreparation class
    data_preparation.initiate_data_preparation('artifacts/raw_data.csv')  # Initiate data preparation process
