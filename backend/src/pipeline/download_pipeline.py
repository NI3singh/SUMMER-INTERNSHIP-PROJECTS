import pandas as pd

class Download:
    @staticmethod
    def download_data():
        try:
            df = pd.read_csv(r'artifacts/final_data.csv')  # Read CSV into DataFrame
            df.to_excel("artifacts/final_data.xlsx", index=False)  # Save DataFrame to Excel without index

            print("CSV file successfully converted to Excel.")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
