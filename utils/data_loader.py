import pandas as pd

# Load data from CSV file
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        return f"Error loading data: {e}"
