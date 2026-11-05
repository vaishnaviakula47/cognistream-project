import streamlit as st
import pandas as pd
import os


def show_activity_monitor():

    st.header("Developer Activity Monitoring")

    file_path = "developer_activity.csv"

    if not os.path.exists(file_path):
        st.info("No activity records available.")
        return

    df = pd.read_csv(file_path)

    if df.empty:
        st.warning("Activity file is empty.")
        return

    required_columns = [
        "switch_count",
        "error_count",
        "break_count",
        "session_minutes"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )
        return

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sessions",
        len(df)
    )

    col2.metric(
        "Total Task Switches",
        int(df["switch_count"].sum())
    )

    col3.metric(
        "Total Errors",
        int(df["error_count"].sum())
    )

    st.subheader("Developer Activity Records")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Break Analysis")

    st.bar_chart(df["break_count"])

    st.subheader("Session Duration")

    st.bar_chart(df["session_minutes"])
