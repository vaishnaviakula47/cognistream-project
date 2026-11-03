"""
Cognistream - Developer Activity Trend Analysis
"""

import pandas as pd


def analyze_activity_trends(df):

    if df is None or df.empty:
        return None

    required = [
        "timestamp",
        "session_minutes",
        "switch_count"
    ]

    if not all(col in df.columns for col in required):
        raise ValueError("Required columns are missing")

    data = df.copy()

    data["timestamp"] = pd.to_datetime(
        data["timestamp"], errors="coerce"
    )

    data = data.dropna(subset=["timestamp"])

    if data.empty:
        return None

    data["date"] = data["timestamp"].dt.date

    trends = data.groupby("date").agg(
        total_sessions=("session_minutes", "count"),
        average_session=("session_minutes", "mean"),
        total_switches=("switch_count", "sum")
    ).reset_index()

    trends["average_session"] = (
        trends["average_session"].round(2)
    )

    return trends


if __name__ == "__main__":
    print("Activity trend analysis module ready.")
