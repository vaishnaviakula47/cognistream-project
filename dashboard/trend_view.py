import streamlit as st

from src.trend_analysis import analyze_activity_trends

def show_activity_trends(df):

st.header("Developer Activity Trends")

if df is None or df.empty:
    st.warning("No activity data available.")
    return

try:
    trends = analyze_activity_trends(df)

    if trends is None or trends.empty:
        st.warning("No valid timestamp records found.")
        return

    st.subheader("Daily Session Count")

    st.line_chart(
        trends.set_index("date")["total_sessions"]
    )

    st.subheader("Average Session Duration")

    st.bar_chart(
        trends.set_index("date")["average_session"]
    )

    st.subheader("Daily Task Switching")

    st.line_chart(
        trends.set_index("date")["total_switches"]
    )

    st.subheader("Activity Trend Details")

    st.dataframe(
        trends,
        use_container_width=True
    )

except ValueError as error:
    st.error(str(error))
