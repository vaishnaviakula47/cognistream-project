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
