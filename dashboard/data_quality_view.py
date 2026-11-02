import streamlit as st

def show_data_quality(df):

st.header("Data Quality Analysis")

if df is None or df.empty:
    st.warning("No valid data available.")
    return

col1, col2, col3 = st.columns(3)

col1.metric(
    "Valid Records",
    len(df)
)

col2.metric(
    "Missing Values",
    int(df.isnull().sum().sum())
)

col3.metric(
    "Duplicate Records",
    int(df.duplicated().sum())
)

st.subheader("Dataset Information")

st.write("Total Columns:", len(df.columns))

st.write("Column Names:")

st.write(list(df.columns))

st.subheader("Validated Dataset")

st.dataframe(
    df,
    use_container_width=True
)
