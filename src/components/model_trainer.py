import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sc

from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

from src.components import data_ingestion 
from src.components import data_preparation 
from src.components import data_transformation
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def scale_data(self, x_train, x_test):
        try:
            scaler = StandardScaler()
            x_scaled_train = scaler.fit_transform(x_train)
            x_scaled_test = scaler.transform(x_test)
            plt.scatter(range(0,len(x_scaled_train)),x_scaled_train)
            plt.scatter(range(0,len(x_scaled_test)),x_scaled_test)

            logging.info("Data scaling completed.")

            return x_scaled_train, x_scaled_test
        except Exception as e:
            raise CustomException(e, sys)

    def train_model(self, x_scaled_train):
        try:
            cluster = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')
            cluster.fit(x_scaled_train)
            logging.info("Model training completed.")
            return cluster
        except Exception as e:
            raise CustomException(e, sys)

    def plot_dendrogram(self, x_scaled, title):
        plt.figure(figsize=(20, 7))
        plt.title(title)
        sc.dendrogram(sc.linkage(x_scaled, method='ward'))
        plt.xlabel('Sample Index')
        plt.ylabel('Euclidean Distance')
        plt.show()

    def plot_cluster(self, x_scaled, x, cluster_labels):
        plt.scatter(range(len(x_scaled)), x, c=cluster_labels)
        plt.title("Clustered Data")
        plt.show()

    def calculate_trend(self, scores):
        X = np.arange(len(scores)).reshape(-1, 1)
        y = scores

        model = LinearRegression()
        model.fit(X, y)
        trend = model.coef_[0]

        return trend

    def evaluate_model(self, data, feature_math):
        try:
            new_data = data[feature_math]
            trends = [self.calculate_trend(new_data.loc[i].dropna()) for i in range(len(new_data))]
            improvement_status = ["Improving" if x > 0 else "Declining" if x < 0 else "Stable" for x in trends]
            final_data = new_data.copy()
            final_data['Improvement Status'] = improvement_status
            final_data['Overall Performance'] = new_data.mean(axis=1)
            logging.info("Evaluation completed.")
            return final_data
        except Exception as e:
            raise CustomException(e, sys)

    def save_model(self, model):
        try:
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=model)
            logging.info("Model saved successfully.")
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_training(self, train_data_reshaped, test_data_reshaped, feature_all):
        try:
            logging.info("Model Training has been initiated")

            logging.info(f"train_data_reshaped shape: {train_data_reshaped.shape}")
            logging.info(f"test_data_reshaped shape: {test_data_reshaped.shape}")
            logging.info(f"feature_all: {feature_all}")

            final_train_data = self.evaluate_model(pd.DataFrame(train_data_reshaped, columns=feature_all), feature_all)
            final_test_data = self.evaluate_model(pd.DataFrame(test_data_reshaped, columns=feature_all), feature_all)

            x_train = final_train_data['Overall Performance'].values.reshape(-1, 1)
            x_test = final_test_data['Overall Performance'].values.reshape(-1, 1)

            x_scaled_train, x_scaled_test = self.scale_data(x_train, x_test)

            self.plot_dendrogram(x_scaled_train, "Training Data Dendrogram")
            self.plot_dendrogram(x_scaled_test, "Testing Data Dendrogram")

            cluster_model = self.train_model(x_scaled_train)

            final_train_data['Cluster'] = cluster_model.labels_
            performance = ['Strong' if i == 0 else 'Moderate' if i == 1 else 'Weak' for i in cluster_model.labels_]
            final_train_data['Performance'] = performance

            self.plot_cluster(x_scaled_train, final_train_data['Overall Performance'], cluster_model.labels_)
            self.save_model(cluster_model)

            logging.info("Model training and evaluation completed.")

            return final_test_data, final_train_data

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    from src.components.data_transformation import DataTransformation

    train_data_path = 'artifacts/train_reshaped.csv'
    test_data_path = 'artifacts/test_reshaped.csv'
    data_transformation_obj = data_transformation.DataTransformation()
    data_transformation_obj = DataTransformation()
    train_data_reshaped, test_data_reshaped, new_data_feature = data_transformation_obj.get_data_transformer_object('artifacts/train.csv', 'artifacts/test.csv')

    model_trainer_obj = ModelTrainer()
    model_trainer_obj.initiate_model_training(train_data_reshaped, test_data_reshaped, new_data_feature)
