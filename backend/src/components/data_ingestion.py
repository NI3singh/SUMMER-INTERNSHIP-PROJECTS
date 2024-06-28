# Import necessary libraries and modules
import os
import sys
from src.exception import CustomException  # Importing custom exception handler
from src.logger import logging  # Importing logging module
import pandas as pd  # Importing pandas for data manipulation

from dataclasses import dataclass  # Importing dataclass for configuration handling
from src.components import data_preparation  # Importing data preparation component
from src.components import data_transformation  # Importing data transformation component

# Define dataclass for configuration
@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', "raw_data.csv")  # Default path for raw data storage

# Define DataIngestion class for handling data ingestion process
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()  # Initialize with default configuration

    def initiate_data_ingestion(self, enr):
        logging.info("Entered the Data Ingestion Method")  # Log entry into method
        print(enr)  # Print enrollment number (debugging or informational)

        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(r'notebook/data/StudentDataset.csv')
            logging.info("Successfully Read the Dataset as Dataframe")  # Log successful read

            # Assign unique IDs to each row in the DataFrame
            df['Id'] = [i for i in range(len(df))]
            logging.info("Indexing of ID column is completed")  # Log completion of indexing

            # Clean column names by removing extra spaces
            for column in df.columns:
                if " '" in column:
                    df.rename(columns={column: column.replace(" '","")}, inplace=True)

            # Filter dataset based on enrollment number (enr)
            dataset = df[df['Current Year (17/18)'] == df['Current Year (17/18)'][enr]]

            # Create directories if they don't exist, then save filtered dataset to CSV
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            dataset.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Ingestion of the Data is Completed")  # Log completion of data ingestion

            return self.ingestion_config.raw_data_path  # Return path to the ingested raw data

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception with the caught error

# Entry point of the script
if __name__ == "__main__":
    enr = int(sys.argv[1])  # Retrieve enrollment number from command-line arguments
    obj = DataIngestion()  # Create instance of DataIngestion class
    raw_data_path = obj.initiate_data_ingestion(enr)  # Initiate data ingestion and retrieve raw data path