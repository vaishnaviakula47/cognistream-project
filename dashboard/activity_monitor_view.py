
import streamlit as st
import pandas as pd


def show_activity_monitor(df=None):

    st.header("Developer Activity Monitoring")

    if df is None or df.empty:
        st.info("Upload a developer activity CSV to view monitoring.")
        return

    required_columns = [
        "switch_count",
        "interruptions",
        "break_minutes",
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

    col1.metric("Total Sessions", len(df))

    col2.metric(
        "Total Task Switches",
        int(df["switch_count"].sum())
    )

    col3.metric(
        "Total Interruptions",
        int(df["interruptions"].sum())
    )

    st.subheader("Developer Activity Records")

    st.dataframe(df, use_container_width=True)

    st.subheader("Break Analysis")
    st.bar_chart(df["break_minutes"])

    st.subheader("Session Duration")
    st.bar_chart(df["session_minutes"])
