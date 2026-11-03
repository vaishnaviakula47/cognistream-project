"""
Cognistream - Analytics Report Generator
"""

import pandas as pd


def generate_activity_report(df):

    if df is None or df.empty:
        return None

    report = {
        "total_sessions": len(df),

        "average_session_minutes": round(
            df["session_minutes"].mean(), 2
        ),

        "total_task_switches": int(
            df["switch_count"].sum()
        ),

        "total_errors": int(
            df["error_count"].sum()
        )
    }

    if "focus_indicator" in df.columns:
        report["focus_distribution"] = (
            df["focus_indicator"]
            .value_counts()
            .to_dict()
        )

    if "cognitive_load" in df.columns:
        report["cognitive_load_distribution"] = (
            df["cognitive_load"]
            .value_counts()
            .to_dict()
        )

    return report


def save_report(report, file_path):

    if report is None:
        return False

    report_df = pd.DataFrame(
        list(report.items()),
        columns=["Metric", "Value"]
    )

    report_df.to_csv(
        file_path,
        index=False
    )

    return True


if __name__ == "__main__":
    print("Cognistream report generator ready.")
