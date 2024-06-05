import pandas as pd
import numpy as np
from dataclasses import dataclass
import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataPreparationConfig:
    preparation_obj_file_path: str = os.path.join('artifacts', "preparation.pkl")

class DataPreparation:
    def __init__(self):
        self.data_preparation_config = DataPreparationConfig()
        
    def initiate_data_preparation(self, train_data_path, test_data_path):
        try:
            # Load datasets
            dataset = pd.read_csv(train_data_path)
            dataset.index

            dataset['Id'] = [i for i in range(len(dataset))]
            dataset.set_index('Id', inplace=True)

            # Step 1: Finding Missing Values
            features_na = [feature for feature in dataset.columns if dataset[feature].isnull().sum() > 1]
            logging.info(f"Features with missing values: {features_na}")
            for feature in features_na:
                logging.info(f"{feature}: {np.round(dataset[feature].isnull().mean(), 4)}% missing values")

            # Step 2: Replace Missing Values with NaN

            def is_float(string):
                try:
                    float(string)
                    return True
                except ValueError:
                    return False

            feature_float = [feature for feature in dataset.columns if 'exam' in feature and dataset[feature].dtypes == 'O']
            logging.info(f"Float features: {feature_float}")
            for feature in feature_float:
                dataset[feature] = dataset[feature].apply(lambda x: x if is_float(x) else np.nan)
                dataset[feature] = dataset[feature].astype(float)


            # Step 3: Convert Datatype of Columns to necessary one
            for feature in feature_float:
                dataset[feature] = dataset[feature].astype(float)

            dataset.info()

            # Step 4: Distinguish Categorical features and Numerical features
            numerical_features = [feature for feature in dataset.columns if dataset[feature].dtypes != 'O']
            logging.info(f"Numerical features: {numerical_features}")
            logging.info(dataset[numerical_features].head())

            categorical_features = [feature for feature in dataset.columns if dataset[feature].dtypes == 'O']
            logging.info(f"Categorical features: {categorical_features}")
            logging.info(dataset[categorical_features].head())

            # Step 5: Replace NaN values with suitable values
            numerical_with_nan = [feature for feature in dataset.columns if dataset[feature].isnull().sum() > 1 and dataset[feature].dtypes != 'O']
            logging.info(f"Numerical features with NaN: {numerical_with_nan}")
            for feature in numerical_with_nan:
                median_value = dataset[feature].median()
                dataset[feature] = dataset[feature].fillna(median_value)
            logging.info(dataset[numerical_with_nan].isnull().sum())

            logging.info("Data preparation completed.")

            # Save the prepared data (optional, you can add this if needed)
            prepared_train_path = os.path.join('artifacts', 'train_prepared.csv')
            prepared_test_path = os.path.join('artifacts', 'test_prepared.csv')
            dataset.to_csv(prepared_train_path, index=False)
            # Assuming test data preparation is similar
            test_data = pd.read_csv(test_data_path)
            test_data.to_csv(prepared_test_path, index=False)

            preparation = {
                'numerical_features': numerical_features,
                'categorical_features': categorical_features,
                # Add any other relevant data you want to save
            }

            # Save the preparation object
            save_object(
                file_path=self.data_preparation_config.preparation_obj_file_path,
                obj=preparation
            )
            logging.info(f"Preparation object saved at: {self.data_preparation_config.preparation_obj_file_path}")

            return (
                numerical_features,
                categorical_features,
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_preparation = DataPreparation()
    data_preparation.initiate_data_preparation('artifacts/train.csv', 'artifacts/test.csv')

    
