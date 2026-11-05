import os
import tempfile

import streamlit as st

from src.main import run_pipeline

from dashboard.activity_monitor_view import show_activity_monitor
from dashboard.data_quality_view import show_data_quality
from dashboard.trend_view import show_activity_trends
from dashboard.report_view import show_report
from dashboard.database_view import show_database_dashboard


st.set_page_config(
    page_title="CogniStream Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("CogniStream")
st.subheader("Developer Flow State & Cognitive Load Analytics")

st.info(
    "CogniStream analyzes developer activity data to estimate "
    "focus indicators, cognitive load, interruptions, and work patterns."
)

st.sidebar.title("Dashboard")
st.sidebar.write("Upload your developer activity dataset to begin.")

uploaded_file = st.file_uploader(
    "Upload Developer Activity CSV",
    type=["csv"]
)

df = None

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

        if df is None or df.empty:
            st.warning("No valid activity records found.")

    except Exception as error:
        st.error(f"Unable to process uploaded data: {error}")

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

else:
    st.info("Please upload your sample_activity.csv file.")

st.divider()

# 1. Developer Activity Overview

st.header("Developer Activity Overview")

if df is not None and not df.empty:

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sessions", len(df))

    col2.metric(
        "Average Session",
        f"{df['session_minutes'].mean():.2f} min"
    )

    col3.metric(
        "Total Task Switches",
        int(df["switch_count"].sum())
    )

    # 2. Flow State Analysis

    st.header("Flow State Analysis")

    st.bar_chart(df["focus_indicator"].value_counts())

    # 3. Cognitive Load Analysis

    st.header("Estimated Cognitive Load")

    st.bar_chart(df["cognitive_load"].value_counts())

    st.subheader("Processed Activity Records")

    st.dataframe(df, use_container_width=True)

st.divider()

# 4. Activity Monitoring

show_activity_monitor(df)

st.divider()

# 5. Data Quality

show_data_quality(df)

st.divider()

# 6. Activity Trends

show_activity_trends(df)

st.divider()

# 7. Report Generation

show_report(df)

st.divider()

# 8. Database Dashboard

show_database_dashboard()

st.divider()

st.caption(
    "CogniStream | Developer Flow-State & Cognitive Load Analytics"
)
