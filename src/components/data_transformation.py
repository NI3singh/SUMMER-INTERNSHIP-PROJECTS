import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = [
                "Age as of Academic Year 17/18" , "Math-exam", "Science-exam ", "English-exam ", 
                "Math19-1", "Science19-1", "English19-1", 
                "Math19-2", "Science19-2", "English19-2", 
                "Math19-3", "Science19-3", "English19-3",
                "Math20-1", "Science20-1", "English20-1",
                "Math20-2", "Science20-2", "English20-2",
                "Math20-3", "Science20-3", "English20-3" ,
            ]

            categorical_columns = [
                "Gender", "Current Year (17/18)", "Proposed Year/Grade (18/19)", 
                "Year of Admission", "Previous Curriculum (17/18)2", "Current School", 
                "Current Curriculum", "Previous year/Grade",
            ]
            
            num_pipeline= Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            logging.info(f"Numerical Columns:{numerical_columns}")
            logging.info(f"Categorical Columns: {categorical_columns}")

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline , numerical_columns),
                    ("cat_pipeline", cat_pipeline , categorical_columns),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
    

    def initiate_data_transformation(self,train_path, test_path):
        
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read Train and Test data Completed")
            logging.info("Obtaining Preprocessing")

            preprocessing_obj=self.get_data_transformer_object()

            train_df['Current Year (17/18)'].unique()
            dataset=train_df.rename(columns={'Current Year (17/18)':'Grade'})

            test_df['Current Year (17/18)'].unique()
            dataset=test_df.rename(columns={'Current Year (17/18)':'Grade'})

            feature_exam = [feature for feature in dataset.columns if 'Math' in feature or 'Science' in feature or 'English' in feature]

            new_data_feature=feature_exam +['Grade']

            data=dataset[new_data_feature]  

            feature_math = [feature for feature in data.columns if 'Math' in feature]

            feature_science = [feature for feature in data.columns if 'Science' in feature]

            feature_english = [feature for feature in data.columns if 'English' in feature]

            logging.info("Applying preprocessing object")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("Saved Processing objects")
            return(
                feature_english,
                feature_math,
                feature_science,
            )
        except Exception as e:
            raise CustomException(e,sys)
