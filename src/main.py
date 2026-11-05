
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

    # Map Vaishnavi's CSV column names to pipeline names.
    column_mapping = {
        "coding_minutes": "session_minutes",
        "context_switches": "switch_count",
    }
    df = df.rename(columns=column_mapping)

    df = clean_activity_data(df)

    if df is None or df.empty:
        return None

    required = {"session_minutes", "switch_count"}

    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    df["session_minutes"] = pd.to_numeric(
        df["session_minutes"], errors="coerce"
    )
    df["switch_count"] = pd.to_numeric(
        df["switch_count"], errors="coerce"
    )

    if "error_count" in df.columns:
        df["error_count"] = pd.to_numeric(
            df["error_count"], errors="coerce"
        ).fillna(0)
    else:
        df["error_count"] = 0

    df = df.dropna(
        subset=["session_minutes", "switch_count"]
    ).copy()

    df = df[
        (df["session_minutes"] >= 0)
        & (df["switch_count"] >= 0)
    ].copy()

    if df.empty:
        return None

    df["switches_per_hour"] = df.apply(
        lambda row: calculate_switch_frequency(
            row["switch_count"],
            row["session_minutes"],
        ) if row["session_minutes"] > 0 else 0,
        axis=1,
    )

    df["focus_indicator"] = df.apply(
        lambda row: classify_focus(
            row["session_minutes"],
            row["switches_per_hour"],
        ),
        axis=1,
    )

    df["cognitive_load"] = df.apply(
        lambda row: estimate_cognitive_load(
            row["switches_per_hour"],
            row["error_count"],
            row["session_minutes"],
        ),
        axis=1,
    )

    return df


if __name__ == "__main__":
    print("CogniStream pipeline ready.")
