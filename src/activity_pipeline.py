"""
CogniStream - Activity Pipeline
"""

import os
import pandas as pd

from src.data_processor import clean_activity_data
from src.trend_analysis import analyze_activity_trends


def load_activity_records(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Activity dataset not found."
        )

    df = pd.read_csv(file_path)

    if df.empty:
        return None

    return clean_activity_data(df)


def generate_activity_trends(file_path):

    df = load_activity_records(file_path)

    if df is None:
        return None

    # Match the actual sample CSV column names.
    df = df.rename(columns={
        "coding_minutes": "session_minutes",
        "context_switches": "switch_count"
    })

    return analyze_activity_trends(df)


if __name__ == "__main__":

    result = generate_activity_trends(
        "data/sample_activity.csv"
    )

    if result is not None:
        print(result)
    else:
        print("No activity records available.")
