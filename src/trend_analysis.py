"""
CogniStream - Developer Activity Trend Analysis
"""

import pandas as pd


def analyze_activity_trends(df):

    if df is None or df.empty:
        return None

    required = [
        "date",
        "session_minutes",
        "switch_count"
    ]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Required columns are missing: {missing}"
        )

    data = df.copy()

    data["date"] = pd.to_datetime(
        data["date"], errors="coerce"
    )

    data = data.dropna(subset=["date"])

    if data.empty:
        return None

    data["date"] = data["date"].dt.date

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
    print("CogniStream trend analysis module ready.")
