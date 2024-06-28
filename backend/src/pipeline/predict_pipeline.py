import sys
import pandas as pd
import pickle
from src.exception import CustomException
from src.utils import load_object

class FetchData:
    @staticmethod
    def fetch():
        try:
            df = pd.read_csv('artifacts/final_data.csv')  # Read final data CSV into a DataFrame

            feature_terms = [feature for feature in df.columns if 'Term' in feature]  # Find columns containing 'Term'

            with open('artifacts/transformed_data.pkl', 'rb') as f:
                data = pickle.load(f)  # Load transformed data from pickle file

            # Count occurrences of unique values in 'Performance', 'Math Performance', 'Science Performance', 'English Performance'
            clusters_performance = df['Performance'].value_counts().to_frame().transpose()
            clusters_math = df['Math Performance'].value_counts().to_frame().transpose()
            clusters_science = df['Science Performance'].value_counts().to_frame().transpose()
            clusters_english = df['English Performance'].value_counts().to_frame().transpose()

            return df, feature_terms, data, clusters_performance, clusters_math, clusters_science, clusters_english

        except Exception as e:
            raise CustomException(e, sys)