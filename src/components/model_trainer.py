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

from sklearn.model_selection import train_test_split

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')
    reshaped_train_path: str = os.path.join('artifacts', "reshaped_train.csv")
    reshaped_test_path: str = os.path.join('artifacts', "reshaped_test.csv")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def split_data(self, raw_data_reshaped, new_data_feature):
        try:
            os.makedirs(os.path.dirname(self.model_trainer_config.reshaped_train_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.model_trainer_config.reshaped_test_path), exist_ok=True)

            train_data_reshaped, test_data_reshaped = train_test_split(raw_data_reshaped, test_size=0.2, random_state=42)
            
            train_data_reshaped_df = pd.DataFrame(train_data_reshaped, columns=new_data_feature)
            test_data_reshaped_df = pd.DataFrame(test_data_reshaped, columns=new_data_feature)

            train_data_reshaped_df.to_csv(self.model_trainer_config.reshaped_train_path, index=False, header=True)
            test_data_reshaped_df.to_csv(self.model_trainer_config.reshaped_test_path, index=False, header=True)

            logging.info("Splitting of Training and Testing Data is completed")
            
            print("Train data:", train_data_reshaped)
            print("Test data:", test_data_reshaped)

            return train_data_reshaped, test_data_reshaped

        except Exception as e:
            raise CustomException(e, sys)

    def scale_data(self, train_data_reshaped, test_data_reshaped):
        try:
            scaler = StandardScaler()
            scaled_train = scaler.fit_transform(train_data_reshaped)
            scaled_test = scaler.transform(test_data_reshaped)
            
            plt.figure(figsize=(10, 6))
            plt.scatter(range(0, len(scaled_train)), scaled_train, label='Scaled Train Data')
            plt.title('Scaled Train Data')
            plt.xlabel('Index')
            plt.ylabel('Value')
            plt.grid(True)
            plt.show()

        
            plt.figure(figsize=(10, 6))
            plt.scatter(range(0, len(scaled_test)), scaled_test, label='Scaled Test Data')
            plt.title('Scaled Test Data')
            plt.xlabel('Index')
            plt.ylabel('Value')
            plt.grid(True)
            plt.show()

            logging.info("Data scaling completed.")

            return scaled_train, scaled_test
        except Exception as e:
            raise CustomException(e, sys)


    def train_model(self, scaled_train):
        try:
            cluster = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')
            cluster.fit(scaled_train)
            logging.info("Model training completed.")
            return cluster
        except Exception as e:
            raise CustomException(e, sys)

    def plot_dendrogram(self, scaled_train, title):
        plt.figure(figsize=(20, 7))
        plt.title(title)
        sc.dendrogram(sc.linkage(scaled_train, method='ward'))
        plt.xlabel('Sample Index')
        plt.ylabel('Euclidean Distance')
        plt.show()

    def plot_cluster(self, scaled_test, x, cluster_labels):
        plt.scatter(range(len(scaled_test)), x, c=cluster_labels)
        plt.title("Clustered Data")
        plt.show()

    def calculate_trend(self, scores):
        X = np.arange(len(scores)).reshape(-1, 1)
        y = scores

        model = LinearRegression()
        model.fit(X, y)
        trend = model.coef_[0]

        return trend

    def evaluate_model(self, raw_data, feature_math):
        try:
            new_data = raw_data[feature_math]
            trends = [self.calculate_trend(new_data.loc[i].dropna()) for i in range(len(new_data))]
            improvement_status = ["Improving" if x > 0 else "Declining" if x < 0 else "Stable" for x in trends]
            final_data = new_data.copy()
            final_data['Improvement Status'] = improvement_status
            final_data['Overall Performance'] = new_data.mean(axis=1)
            print(final_data)
            logging.info("Evaluation completed.")
            return final_data
        except Exception as e:
            raise CustomException(e, sys)
        
    def plot_student_performance(self, student_id, new_data):
        try:
            plt.plot(list(new_data.columns), list(new_data.loc[student_id]))
            plt.title(f'Student Performance for ID {student_id}')
            plt.xlabel('Exams')
            plt.ylabel('Scores')
            plt.show()
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_model(self, model):
        try:
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=model)
            logging.info("Model saved successfully.")
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_training(self, new_data_feature, train_data_reshaped, test_data_reshaped):
        try:
            logging.info("Model Training has been initiated")

            final_train_data = self.evaluate_model(pd.DataFrame(train_data_reshaped, columns=new_data_feature), new_data_feature)
            final_test_data = self.evaluate_model(pd.DataFrame(test_data_reshaped, columns=new_data_feature), new_data_feature)

            x_train = final_train_data['Overall Performance'].values.reshape(-1, 1)
            x_test = final_test_data['Overall Performance'].values.reshape(-1, 1)

            new_scaled_train, new_scaled_test = self.scale_data(x_train, x_test)

            self.plot_dendrogram(new_scaled_train, "Training Data Dendrogram")
            self.plot_dendrogram(new_scaled_test, "Testing Data Dendrogram")

            cluster_model = self.train_model(new_scaled_train)

            final_train_data['Cluster'] = cluster_model.labels_
            performance = ['Strong' if i == 0 else 'Moderate' if i == 1 else 'Weak' for i in cluster_model.labels_]
            final_train_data['Performance'] = performance

            self.plot_cluster(new_scaled_train, final_train_data['Overall Performance'], cluster_model.labels_)
            self.save_model(cluster_model)

            student_id = int(input("Enter the student ID to plot performance: "))
            self.plot_student_performance(student_id, final_train_data[new_data_feature])

            logging.info("Model training and evaluation completed.")

            return final_test_data, final_train_data

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":

    data_transformation_obj = data_transformation.DataTransformation()
        
    # Load and transform raw data
    raw_data_path = 'artifacts/data.csv'
    raw_data_reshaped, new_data_feature, raw_data = data_transformation_obj.get_data_transformer_object(raw_data_path)
        
    # Initialize Model Trainer
    model_trainer_obj = ModelTrainer()

    # Split the reshaped data
    train_data_reshaped, test_data_reshaped = model_trainer_obj.split_data(raw_data_reshaped, new_data_feature)

    # Initiate model training
    model_trainer_obj.initiate_model_training(new_data_feature, train_data_reshaped, test_data_reshaped)
