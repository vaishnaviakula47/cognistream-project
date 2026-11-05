"""
CogniStream - Developer Activity Analysis
"""

import pandas as pd


def analyze_activity(df):

    if df is None or df.empty:
        return None

    required_columns = [
        "session_minutes",
        "switch_count",
        "interruptions"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Required columns are missing: {missing}"
        )

    result = {}

    result["total_sessions"] = len(df)

    result["average_session"] = round(
        df["session_minutes"].mean(), 2
    )

    result["total_switches"] = int(
        df["switch_count"].sum()
    )

    result["average_switches"] = round(
        df["switch_count"].mean(), 2
    )

    result["total_interruptions"] = int(
        df["interruptions"].sum()
    )

    return result


if __name__ == "__main__":

    sample = pd.DataFrame({
        "session_minutes": [30, 45, 60],
        "switch_count": [2, 4, 5],
        "interruptions": [1, 2, 3]
    })

    print(analyze_activity(sample))
