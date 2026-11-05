import streamlit as st
import pandas as pd

from src.report_generator import generate_activity_report


def show_report(df):

    st.header("Developer Analytics Report")

    if df is None or df.empty:
        st.warning("No analytics data available.")
        return

    try:
        report = generate_activity_report(df)

        if report is None:
            st.warning("Unable to generate report.")
            return

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Sessions",
                report["total_sessions"]
            )

        with col2:
            st.metric(
                "Average Session",
                f"{report['average_session_minutes']} min"
            )

        st.subheader("Activity Summary")
        st.json(report)

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Activity Report",
            data=csv_data,
            file_name="cognistream_activity_report.csv",
            mime="text/csv"
        )

    except (ValueError, KeyError, TypeError) as error:
        st.error(f"Unable to generate report: {error}")
