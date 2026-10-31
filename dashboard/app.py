import streamlit as st
import pandas as pd

st.set_page_config(
page_title="CogniStream Analytics",
layout="wide"
)

st.title("CogniStream")
st.subheader("Developer Flow State & Cognitive Load Analytics")

st.info(
"Prototype dashboard using sample activity data. "
"Metrics are estimates, not mental-health assessments."
)

uploaded_file = st.file_uploader(
"Upload developer activity CSV",
type=["csv"]
)

if uploaded_file is not None:
try:
df = pd.read_csv(uploaded_file)

    st.subheader("Activity Data")
    st.dataframe(df, use_container_width=True)

    st.subheader("Dataset Summary")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Records", len(df))

    with col2:
        st.metric("Total Features", len(df.columns))

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:
        selected_column = st.selectbox(
            "Choose a metric to visualize",
            numeric_columns
        )

        st.line_chart(df[selected_column])
    else:
        st.warning(
            "No numeric columns found to visualize."
        )

except Exception as error:
    st.error(f"Unable to read the CSV file: {error}")

else:
st.write("Upload a sample CSV file to begin analysis.")
import os
import tempfile

import pandas as pd
import streamlit as st

from src.main import run_pipeline

st.set_page_config(
page_title="CogniStream Analytics",
layout="wide",
)

st.title("CogniStream")
st.subheader(
"Developer Flow State & Cognitive Load Analytics"
)

st.caption(
"Prototype using uploaded activity data. "
"Focus indicators are heuristic estimates."
)

uploaded_file = st.file_uploader(
"Upload developer activity CSV",
type=["csv"],
)

if uploaded_file is not None:
raw_data = pd.read_csv(uploaded_file)
temp_path = None

try:
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
    ) as temp_file:
        raw_data.to_csv(temp_file.name, index=False)
        temp_path = temp_file.name

    df = run_pipeline(temp_path)

except Exception as exc:
    st.error(f"Could not process the uploaded CSV: {exc}")
    df = None

finally:
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)

if df is not None and not df.empty:
    required_columns = [
        "session_minutes",
        "switches_per_hour",
        "focus_indicator",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "The processed data is missing required columns: "
            + ", ".join(missing_columns)
        )
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Activity Records", len(df))

        with col2:
            st.metric(
                "Average Session (min)",
                round(df["session_minutes"].mean(), 2),
            )

        with col3:
            st.metric(
                "Average Switches / Hour",
                round(df["switches_per_hour"].mean(), 2),
            )

        st.subheader("Focus Indicator Distribution")
        st.bar_chart(
            df["focus_indicator"].value_counts()
        )

        st.subheader("Processed Activity Data")
        st.dataframe(df, use_container_width=True)

else:
    st.warning(
        "No valid data was processed. "
        "Check the CSV columns and values."
    )

else:
st.info(
"Upload a CSV containing session_minutes "
"and switch_count to begin."
)
