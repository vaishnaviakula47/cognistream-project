import os
import tempfile

import pandas as pd
import streamlit as st
from dashboard.activity_monitor_view import show_activity_monitor
from src.main import run_pipeline

st.set_page_config(
page_title="CogniStream Analytics",
layout="wide"
)

st.title("CogniStream")

st.subheader(
"Developer Flow State & Cognitive Load Analytics"
)

st.info(
"Prototype analytics based on developer activity data. "
"Focus and cognitive-load indicators are estimates."
)

uploaded_file = st.file_uploader(
"Upload Developer Activity CSV",
type=["csv"]
)

if uploaded_file is not None:
temp_path = None

try:
    with tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=".csv",
        delete=False
    ) as temp_file:

        uploaded_file.seek(0)
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    df = run_pipeline(temp_path)

except Exception as error:
    st.error(f"Unable to process uploaded data: {error}")
    df = None

finally:
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)

if df is not None and not df.empty:

    required_columns = [
        "session_minutes",
        "switch_count",
        "focus_indicator",
        "cognitive_load"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "Missing processed columns: "
            + ", ".join(missing_columns)
        )
    else:
        st.header("Developer Activity Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Sessions",
            len(df)
        )

        col2.metric(
            "Average Session",
            f"{df['session_minutes'].mean():.2f} min"
        )

        col3.metric(
            "Total Task Switches",
            int(df["switch_count"].sum())
        )

        st.header("Flow State Analysis")

        st.bar_chart(
            df["focus_indicator"].value_counts()
        )

        st.header("Cognitive Load Analysis")

        st.bar_chart(
            df["cognitive_load"].value_counts()
        )

        st.header("Developer Activity Details")

        st.dataframe(
            df,
            use_container_width=True
        )

else:
    st.warning(
        "Unable to process the uploaded dataset."
    )

else:
st.info("Upload a CSV file to view analytics.")
st.divider()

st.title("Developer Activity Monitoring")

show_activity_monitor()
