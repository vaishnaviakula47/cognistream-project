import os
import pandas as pd

from src.trend_analysis import analyze_activity_trends


def load_activity_records(file_path="developer_activity.csv"):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Developer activity file not found"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        return None

    return df


def generate_activity_trends(file_path="developer_activity.csv"):

    df = load_activity_records(file_path)

    if df is None:
        return None

    trends = analyze_activity_trends(df)

    return trends


if __name__ == "__main__":

    result = generate_activity_trends()

    if result is not None:
        print(result)
    else:
        print("No activity records available.")
