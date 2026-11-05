import streamlit as st

from src.database import (
    create_database,
    get_all_activities
)


def show_database_dashboard():

    st.header("Developer Activity Database")

    create_database()

    df = get_all_activities()

    if df is None or df.empty:

        st.info("No database records available.")

        return

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Stored Sessions",
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

    st.subheader("Stored Developer Activities")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Session Duration Analysis")

    st.bar_chart(
        df["session_minutes"]
    )

    st.subheader("Task Switching Analysis")

    st.bar_chart(
        df["switch_count"]
    )

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Database Records",
        data=csv_data,
        file_name="cognistream_database_records.csv",
        mime="text/csv"
    )
