import pandas as pd

from src.data_processor import (
    load_activity_data,
    clean_activity_data,
)
from src.feature_calculator import calculate_switch_frequency
from src.flow_state import classify_focus
from src.cognitive_load import estimate_cognitive_load


def run_pipeline(file_path):

    df = load_activity_data(file_path)

    if df is None or df.empty:
        return None

    df = clean_activity_data(df)

    if df is None or df.empty:
        return None

    # Map CSV column names to standard pipeline names.
    column_mapping = {
        "coding_minutes": "session_minutes",
        "context_switches": "switch_count"
    }

    df = df.rename(columns=column_mapping)

    required = [
        "session_minutes",
        "switch_count",
        "interruptions"
    ]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # Convert activity columns into numeric values.
    numeric_columns = [
        "session_minutes",
        "switch_count",
        "interruptions"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df = df.dropna(
        subset=numeric_columns
    ).copy()

    df = df[
        (df["session_minutes"] >= 0)
        & (df["switch_count"] >= 0)
        & (df["interruptions"] >= 0)
    ].copy()

    if df.empty:
        return None

    # Calculate task switches per hour.
    df["switches_per_hour"] = df.apply(
        lambda row: calculate_switch_frequency(
            row["switch_count"],
            row["session_minutes"]
        ),
        axis=1
    )

    # Calculate focus indicator.
    df["focus_indicator"] = df.apply(
        lambda row: classify_focus(
            row["session_minutes"],
            row["switches_per_hour"]
        ),
        axis=1
    )

    # Estimate cognitive load using interruptions.
    df["cognitive_load"] = df.apply(
        lambda row: estimate_cognitive_load(
            row["switches_per_hour"],
            row["interruptions"],
            row["session_minutes"]
        ),
        axis=1
    )

    return df


if __name__ == "__main__":
    print("CogniStream pipeline ready.")
