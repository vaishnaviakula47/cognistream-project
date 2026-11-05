import pandas as pd

from data_processor import (
    load_activity_data,
    clean_activity_data,
)
from feature_calculator import (
    calculate_switch_frequency,
)
from flow_state import classify_focus


def run_pipeline(file_path):
    df = load_activity_data(file_path)

    if df is None:
        return None

    df = clean_activity_data(df)

    if df is None or df.empty:
        print("No usable activity data.")
        return None

    required = {
        "session_minutes",
        "switch_count",
    }

    if not required.issubset(df.columns):
        print("Missing required columns:", required - set(df.columns))
        return None

    df["session_minutes"] = pd.to_numeric(
        df["session_minutes"], errors="coerce"
    )
    df["switch_count"] = pd.to_numeric(
        df["switch_count"], errors="coerce"
    )

    df = df.dropna(
        subset=["session_minutes", "switch_count"]
    ).copy()

    df = df[
        (df["session_minutes"] >= 0)
        & (df["switch_count"] >= 0)
    ]

    if df.empty:
        print("No valid activity records.")
        return None

    df["switches_per_hour"] = df.apply(
        lambda row: calculate_switch_frequency(
            row["switch_count"],
            row["session_minutes"],
        ),
        axis=1,
    )

    df["focus_indicator"] = df.apply(
        lambda row: classify_focus(
            row["session_minutes"],
            row["switches_per_hour"],
        ),
        axis=1,
    )

    return df
    if _name_ == "_main_":
    print("Cognistream pipeline ready.")
