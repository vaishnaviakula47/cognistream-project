"""
CogniStream - Data Validation Module
"""

import pandas as pd

REQUIRED_COLUMNS = [
    "session_minutes",
    "switch_count",
    "interruptions"
]


def validate_activity_data(df):

    if df is None or df.empty:
        return None

    df = df.copy()

    # Normalize column names
    df.columns = (
        df.columns.str.strip().str.lower()
    )

    # Check required columns
    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # Convert values to numeric
    for col in REQUIRED_COLUMNS:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    # Remove invalid records
    df = df.dropna(
        subset=REQUIRED_COLUMNS
    )

    # Remove negative values
    df = df[
        (df[REQUIRED_COLUMNS] >= 0).all(axis=1)
    ].copy()

    return df.reset_index(drop=True)


if __name__ == "__main__":
    print("CogniStream data validation ready.")
