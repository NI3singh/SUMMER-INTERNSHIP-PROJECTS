import sys  # Import sys for system-specific parameters and functions
import os  # Import os for operating system dependent functionality
import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import scipy.cluster.hierarchy as sc  # Import scipy for hierarchical clustering

from dataclasses import dataclass  # Import dataclass for configuration handling
from sklearn.linear_model import LinearRegression  # Import LinearRegression for trend calculation
from sklearn.preprocessing import StandardScaler  # Import StandardScaler for data scaling
from sklearn.cluster import AgglomerativeClustering  # Import AgglomerativeClustering for clustering

from src.components import data_ingestion  # Import data ingestion component
from src.components import data_preparation  # Import data preparation component
from src.components import data_transformation  # Import data transformation component
from src.logger import logging  # Import logging module for logging messages
from src.exception import CustomException  # Import custom exception handler
from src.utils import save_object  # Import utility function to save objects
from sklearn.model_selection import train_test_split  # Import train_test_split for data splitting

# ModelTrainerConfig dataclass to hold configuration options
@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')  # Default path for saving trained model
    final_data_path: str = os.path.join('artifacts', 'final_data.csv')  # Default path for saving final evaluated data

# ModelTrainer class for training and evaluating models
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()  # Initialize with default configuration

    # Method to scale input data using StandardScaler
    def scale_data(self, x_data):
        try:
            scaler = StandardScaler()  # Initialize StandardScaler
            x_scaled_data = scaler.fit_transform(x_data)  # Fit and transform input data

            logging.info("Data scaling completed.")  # Log completion of data scaling

            return x_scaled_data  # Return scaled data
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs during scaling

    # Method to train a clustering model using Agglomerative Clustering
    def train_model(self, x_scaled_train):
        try:
            cluster = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')  # Initialize clustering model
            cluster.fit(x_scaled_train)  # Fit clustering model to scaled training data

            logging.info("Model training completed.")  # Log completion of model training

            return cluster  # Return trained clustering model
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs during model training

    # Method to calculate trend using Linear Regression
    def calculate_trend(self, scores):
        X = np.arange(len(scores)).reshape(-1, 1)  # Create X array for linear regression
        y = scores  # Define y as input scores

        model = LinearRegression()  # Initialize Linear Regression model
        model.fit(X, y)  # Fit model to X and y

        trend = model.coef_[0]  # Calculate trend coefficient

        return trend  # Return calculated trend coefficient

    # Method to evaluate model based on student performance trends
    def evaluate_model(self, data, feature_all, feature_math, feature_science, feature_english):
        try:
            new_data = data[feature_all]  # Select relevant features from data
            math_data = data[feature_math]  # Select math-related features
            science_data = data[feature_science]  # Select science-related features
            english_data = data[feature_english]  # Select english-related features

            # Calculate overall trends for each student
            overall_trends = [self.calculate_trend(new_data.loc[i].dropna()) for i in range(len(new_data))]
            math_trends = [self.calculate_trend(math_data.loc[i].dropna()) for i in range(len(new_data))]
            science_trends = [self.calculate_trend(science_data.loc[i].dropna()) for i in range(len(new_data))]
            english_trends = [self.calculate_trend(english_data.loc[i].dropna()) for i in range(len(new_data))]

            # Determine improvement status based on trends
            improvement_status = ["Improving" if x > 0 else "Declining" if x < 0 else "Stable" for x in overall_trends]
            math_improvement_status = ["Improving" if x > 0 else "Declining" if x < 0 else "Stable" for x in math_trends]
            science_improvement_status = ["Improving" if x > 0 else "Declining" if x < 0 else "Stable" for x in science_trends]
            english_improvement_status = ["Improving" if x > 0 else "Declining" if x < 0 else "Stable" for x in english_trends]

            # Create final evaluated data with improvement status and overall performance
            final_data = new_data.copy()
            final_data['Improvement Status'] = improvement_status
            final_data['Math Improvement Status'] = math_improvement_status
            final_data['Science Improvement Status'] = science_improvement_status
            final_data['English Improvement Status'] = english_improvement_status
            final_data['Overall Performance'] = round(new_data.mean(axis=1), 2)

            logging.info("Evaluation completed.")  # Log completion of evaluation

            return final_data  # Return final evaluated data
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs during evaluation

    # Method to save trained model to file
    def save_model(self, model):
        try:
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=model)  # Save model to file
            logging.info("Model saved successfully.")  # Log successful model save
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs during model save

    # Method to save final evaluated data to CSV file
    def save_file(self, final_new_data):
        try:
            os.makedirs(os.path.dirname(self.model_trainer_config.final_data_path), exist_ok=True)  # Create directory if it doesn't exist
            final_new_data.to_csv(self.model_trainer_config.final_data_path, index=False, header=True)  # Save final data to CSV file
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs during file save

    # Method to initiate model training process
    def initiate_model_training(self, new_data_reshaped, feature_all, feature_math, feature_science, feature_english):
        try:
            logging.info("Model Training has been initiated")  # Log initiation of model training

            logging.info(f"new_data_reshaped shape: {new_data_reshaped.shape}")  # Log shape of reshaped data
            logging.info(f"feature_all: {feature_all}")  # Log list of all features

            # Evaluate model and student performance based on features
            final_new_data = self.evaluate_model(pd.DataFrame(new_data_reshaped, columns=feature_all), feature_all, feature_math, feature_science, feature_english)

            x_data = final_new_data['Overall Performance'].values.reshape(-1, 1)  # Select overall performance data

            x_scaled_data = self.scale_data(x_data)  # Scale overall performance data

            cluster_model = self.train_model(x_scaled_data)  # Train clustering model on scaled data

            # Assign cluster labels and performance categories to final evaluated data
            final_new_data['Cluster'] = cluster_model.labels_
            performance = ['Strong' if i == 0 else 'Moderate' if i == 1 else 'Weak' for i in cluster_model.labels_]
            final_new_data['Performance'] = performance

            data = pd.read_csv("artifacts/raw_data.csv")  # Load raw data for additional features
            final_new_data['Grade'] = data["Current Year (17/18)"]  # Add Grade information to final data
            final_new_data['Id'] = data["Id"]  # Add Id information to final data

            # Calculate term averages and overall subject performances
            for i in range(len(feature_math)):
                feature = feature_math[i].replace("Math", "Term")
                final_new_data[feature] = round((final_new_data[feature_math[i]] + final_new_data[feature_science[i]] + final_new_data[feature_english[i]]) / 3, 2)

            final_new_data['Overall Math Performance'] = round(final_new_data[feature_math].mean(axis=1), 2)
            final_new_data['Overall Science Performance'] = round(final_new_data[feature_science].mean(axis=1), 2)
            final_new_data['Overall English Performance'] = round(final_new_data[feature_english].mean(axis=1), 2)

            # Train clustering models for math, science, and english performances
            cluster_math_model = self.train_model(self.scale_data(final_new_data['Overall Math Performance'].values.reshape(-1, 1)))
            cluster_science_model = self.train_model(self.scale_data(final_new_data['Overall Science Performance'].values.reshape(-1, 1)))
            cluster_english_model = self.train_model(self.scale_data(final_new_data['Overall English Performance'].values.reshape(-1, 1)))

            # Assign performance categories to math, science, and english performances
            performance_math = ['Strong' if i == 0 else 'Moderate' if i == 1 else 'Weak' for i in cluster_math_model.labels_]
            final_new_data['Math Performance'] = performance_math

            performance_science = ['Strong' if i == 0 else 'Moderate' if i == 1 else 'Weak' for i in cluster_science_model.labels_]
            final_new_data['Science Performance'] = performance_science

            performance_english = ['Strong' if i == 0 else 'Moderate' if i == 1 else 'Weak' for i in cluster_english_model.labels_]
            final_new_data['English Performance'] = performance_english

            self.save_model(cluster_model)  # Save main clustering model

            self.save_file(final_new_data)  # Save final evaluated data to CSV

            logging.info("Model training and evaluation completed.")  # Log completion of model training and evaluation

            return final_new_data  # Return final evaluated data

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if an error occurs during model training or evaluation

if __name__ == "__main__":
    from src.components.data_transformation import DataTransformation  # Import DataTransformation class

    train_data_path = 'artifacts/train_reshaped.csv'  # Define path to training data CSV
    test_data_path = 'artifacts/test_reshaped.csv'  # Define path to test data CSV

    data_transformation_obj = DataTransformation()  # Create instance of DataTransformation class
    new_data_reshaped, new_data_feature, feature_math, feature_science, feature_english = data_transformation_obj.get_data_transformer_object('artifacts/raw_data.csv')

    model_trainer_obj = ModelTrainer()  # Create instance of ModelTrainer class
    model_trainer_obj.initiate_model_training(new_data_reshaped, new_data_feature, feature_math, feature_science, feature_english)  # Initiate model training and evaluation
