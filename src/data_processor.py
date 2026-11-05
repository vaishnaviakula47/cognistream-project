"""
Cognistream - Data Processing Module
"""

import pandas as pd


def load_activity_data(file_path):
    """Load developer activity data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("Error: Dataset file not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: Dataset file is empty.")
        return None


def clean_activity_data(df):
    """Clean and validate the activity dataset."""
    if df is None:
        return None

    df = df.drop_duplicates().copy()
    df.columns = df.columns.str.strip()

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )

    return df


if __name__ == "__main__":
    print("Cognistream data processor is ready.")
