
"""
CogniStream - Data Processing Module
"""

import pandas as pd


def load_activity_data(file_path):
    """Load developer activity data from a CSV file."""
    try:
        return pd.read_csv(file_path)

    except FileNotFoundError:
        raise FileNotFoundError("Dataset file not found.")

    except pd.errors.EmptyDataError:
        raise ValueError("Dataset file is empty.")


def clean_activity_data(df):
    """Clean and validate the activity dataset."""
    if df is None:
        return None

    df = df.drop_duplicates().copy()

    df.columns = (
        df.columns.str.strip().str.lower()
    )

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )

    return df


if __name__ == "__main__":
    print("CogniStream data processor is ready.")
