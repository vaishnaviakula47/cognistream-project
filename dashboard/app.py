import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Add project root directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.main import run_pipeline
# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CogniStream | Developer Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM DASHBOARD DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #080f1e 0%,
        #101c32 55%,
        #0b1425 100%
    );
    color: #e8f0fc;
}

[data-testid="stMain"] {
    background: transparent;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101d32,
        #0b1425
    );
    border-right: 1px solid #263b58;
}

[data-testid="stSidebar"] * {
    color: #e8f0fc;
}

[data-testid="stSidebar"] hr {
    border-color: #293d59;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 9px;
    padding: 9px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #203653;
}

.main-title {
    font-size: 36px;
    font-weight: 850;
    letter-spacing: -1px;
    color: #ffffff;
}

.subtitle {
    color: #9db2d0;
    font-size: 15px;
    margin-top: 5px;
}

.section-heading {
    font-size: 25px;
    font-weight: 750;
    color: #ffffff;
    margin-top: 18px;
    margin-bottom: 5px;
}

.section-description {
    color: #9db2d0;
    font-size: 14px;
    margin-bottom: 18px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #192b45,
        #122139
    );
    border: 1px solid #2b4566;
    padding: 20px;
    border-radius: 16px;
    min-height: 125px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.18);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #55aaff;
}

div[data-testid="stMetricLabel"] {
    color: #a8bdd9;
    font-size: 14px;
}

div[data-testid="stMetricValue"] {
    color: #69baff;
    font-size: 29px;
    font-weight: 800;
}

.stButton button,
.stDownloadButton button {
    background: linear-gradient(
        100deg,
        #2563eb,
        #168bd1
    );
    color: white;
    border: none;
    border-radius: 10px;
    padding: 9px 16px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: linear-gradient(
        100deg,
        #3478ff,
        #25a6ed
    );
    border: none;
    transform: translateY(-2px);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: #172941;
    border-color: #304966;
    border-radius: 9px;
}

[data-testid="stDateInput"] label {
    color: #c6d6eb;
    font-weight: 600;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #2b4566;
    border-radius: 13px;
    overflow: hidden;
}

div[data-testid="stVegaLiteChart"],
div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stAltairChart"] {
    background: #14243a;
    border: 1px solid #263f5e;
    border-radius: 14px;
    padding: 12px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #2a405e;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# DATASET LOADING
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "sample_activity.csv"


@st.cache_data
def load_data(file_path, modified_time):

    data = run_pipeline(file_path)

    if data is None:
        return pd.DataFrame()

    return data


if not DATASET_PATH.exists():
    st.error("Dataset not found: data/sample_activity.csv")
    st.stop()


try:
    df = load_data(
        str(DATASET_PATH),
        DATASET_PATH.stat().st_mtime
    )

except Exception as error:
    st.error(f"Dataset processing error: {error}")
    st.stop()


if df is None or df.empty:
    st.warning("No valid activity records found.")
    st.stop()


# =====================================================
# PREPARE DATA
# =====================================================

df = df.copy()

if "date" in df.columns:
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown("# 🧠 CogniStream")

    st.caption("DEVELOPER ANALYTICS PLATFORM")

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Overview",
            "Focus Analytics",
            "Cognitive Load",
            "Activity Monitoring",
            "Trends",
            "Reports",
            "Database"
        ],
        key="main_navigation"
    )

    st.divider()

    st.markdown("### DATA SOURCE")

    st.success("Repository dataset connected")

    st.caption("data/sample_activity.csv")

    st.caption(f"Total records: {len(df)}")

    if st.button(
        "🔄 Refresh Dataset",
        use_container_width=True
    ):

        try:
            load_data.clear()
            st.session_state.pop("main_date_filter", None)

            st.success("Dataset cache cleared.")

            st.rerun()

        except Exception as error:
            st.error(f"Dataset refresh failed: {error}")

    st.divider()

    st.caption("CogniStream v2.0")




# =====================================================
# RESET SCROLL WHEN NAVIGATION CHANGES
# =====================================================

if "previous_page" not in st.session_state:
    st.session_state["previous_page"] = page

if st.session_state["previous_page"] != page:

    st.session_state["previous_page"] = page

    components.html(
        f"""
        <script>
        (() => {{
            const reset = () => {{
                const main = window.parent.document.querySelector(
                    '[data-testid="stMain"]'
                );

                if (main) {{
                    main.scrollTop = 0;
                    main.scrollTo(0, 0);
                }}
            }};

            reset();
            requestAnimationFrame(reset);
            setTimeout(reset, 100);
            setTimeout(reset, 300);
            setTimeout(reset, 700);
        }})();
        </script>
        <div style="display:none">{page}</div>
        """,
        height=0,
        scrolling=False
    )

# =====================================================
# MAIN DASHBOARD HEADER
# =====================================================

st.markdown("""
<div class="main-title">
    🧠 CogniStream Analytics
</div>

<div class="subtitle">
    Developer Flow-State & Cognitive Load Intelligence Platform
</div>

<div style="
    margin-top:18px;
    margin-bottom:22px;
    height:3px;
    width:100%;
    background:linear-gradient(
        90deg,
        #3b82f6,
        #14b8a6,
        transparent
    );
    border-radius:10px;
"></div>
""", unsafe_allow_html=True)


# =====================================================
# GLOBAL DATE FILTER
# =====================================================

filtered_df = df.copy()

if "date" in filtered_df.columns:

    valid_dates = filtered_df["date"].dropna()

    if not valid_dates.empty:

        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        st.markdown("### 📅 Date Filter")

        date_range = st.date_input(
            "Select activity date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="main_date_filter"
        )

        if isinstance(date_range, (tuple, list)):

            if len(date_range) == 2:

                start_date, end_date = date_range

                filtered_df = filtered_df[
                    filtered_df["date"].dt.date.between(
                        start_date,
                        end_date
                    )
                ]

            elif len(date_range) == 1:

                selected_date = date_range[0]

                filtered_df = filtered_df[
                    filtered_df["date"].dt.date == selected_date
                ]

        elif date_range:

            filtered_df = filtered_df[
                filtered_df["date"].dt.date == date_range
            ]

st.caption(
    f"Showing {len(filtered_df)} of {len(df)} activity records"
)

st.divider()


# =====================================================
# COMMON HELPER FUNCTIONS
# =====================================================

def show_metric(label, value, delta=None):

    st.metric(
        label=label,
        value=value,
        delta=delta
    )


def show_page_title(title, description):

    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="section-description">{description}</div>',
        unsafe_allow_html=True
    )


def show_empty_message():

    st.warning(
        "No activity records are available for the selected date range. "
        "Please select another date range."
    )


def show_download_button(data, filename, label):

    csv_data = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )


# =====================================================
# PAGE 1: OVERVIEW
# =====================================================

if page == "Overview":

    show_page_title(
        "Executive Overview",
        "A complete summary of developer activity and productivity indicators."
    )

    if filtered_df.empty:
        show_empty_message()

    else:

        total_sessions = len(filtered_df)

        avg_session = filtered_df["session_minutes"].mean()

        total_switches = int(
            filtered_df["switch_count"].sum()
        )

        total_interruptions = int(
            filtered_df["interruptions"].sum()
        )

        total_tasks = int(
            filtered_df["tasks_completed"].sum()
        )

        # KPI CARDS

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            show_metric("Total Sessions", total_sessions)

        with c2:
            show_metric(
                "Average Session",
                f"{avg_session:.2f} min"
            )

        with c3:
            show_metric("Task Switches", total_switches)

        with c4:
            show_metric("Interruptions", total_interruptions)

        c5, c6 = st.columns(2)

        with c5:
            show_metric("Tasks Completed", total_tasks)

        with c6:
            show_metric(
                "Average Coding Time",
                f"{filtered_df['session_minutes'].mean():.1f} min"
            )

        st.divider()

        # DISTRIBUTION CHARTS

        left, right = st.columns(2)

        with left:

            st.markdown("#### 🎯 Focus Distribution")

            if "focus_indicator" in filtered_df.columns:

                st.bar_chart(
                    filtered_df["focus_indicator"].value_counts(),
                    color="#3B82F6"
                )

        with right:

            st.markdown("#### 🧠 Cognitive Load Distribution")

            if "cognitive_load" in filtered_df.columns:

                st.bar_chart(
                    filtered_df["cognitive_load"].value_counts(),
                    color="#14B8A6"
                )

        st.divider()

        # DEVELOPER SUMMARY

        if "developer_id" in filtered_df.columns:

            st.markdown("#### 👨‍💻 Developer Activity Summary")

            developer_summary = filtered_df.groupby(
                "developer_id"
            ).agg(
                total_sessions=("session_minutes", "count"),
                average_session=("session_minutes", "mean"),
                total_switches=("switch_count", "sum"),
                total_interruptions=("interruptions", "sum"),
                tasks_completed=("tasks_completed", "sum")
            ).round(2)

            st.dataframe(
                developer_summary,
                use_container_width=True
            )

        st.markdown("#### 🕒 Recent Developer Activity")

        st.dataframe(
            filtered_df.tail(10),
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# PAGE 2: FOCUS ANALYTICS
# =====================================================

elif page == "Focus Analytics":

    show_page_title(
        "Focus Analytics",
        "Understand developer concentration and focus indicators."
    )

    if filtered_df.empty:
        show_empty_message()

    else:

        focus_counts = filtered_df[
            "focus_indicator"
        ].value_counts()

        high_focus = int(
            (filtered_df["focus_indicator"] == "High Focus Indicator").sum()
        )

        moderate_focus = int(
            (filtered_df["focus_indicator"] == "Moderate Focus Indicator").sum()
        )

        low_focus = int(
            (filtered_df["focus_indicator"] == "Low Focus Indicator").sum()
        )

        total = len(filtered_df)

        high_percentage = high_focus / total * 100
        moderate_percentage = moderate_focus / total * 100
        low_percentage = low_focus / total * 100

        c1, c2, c3 = st.columns(3)

        with c1:
            show_metric(
                "High Focus",
                high_focus,
                f"{high_percentage:.1f}% of records"
            )

        with c2:
            show_metric(
                "Moderate Focus",
                moderate_focus,
                f"{moderate_percentage:.1f}% of records"
            )

        with c3:
            show_metric(
                "Low Focus",
                low_focus,
                f"{low_percentage:.1f}% of records"
            )

        st.divider()

        left, right = st.columns(2)

        with left:

            st.markdown("#### Focus Category Distribution")

            st.bar_chart(
                focus_counts,
                color="#3B82F6"
            )

        with right:

            st.markdown("#### Focus Percentage")

            percentages = (
                focus_counts / total * 100
            ).round(2)

            st.bar_chart(
                percentages,
                color="#8B5CF6"
            )

        st.markdown("#### Developer Focus Records")

        st.dataframe(
            filtered_df[
                [
                    "developer_id",
                    "session_minutes",
                    "switches_per_hour",
                    "focus_indicator"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Focus indicators are preliminary classifications "
            "based on project-defined rules."
        )


# =====================================================
# PAGE 3: COGNITIVE LOAD
# =====================================================

elif page == "Cognitive Load":

    show_page_title(
        "Cognitive Load Analytics",
        "Analyze estimated cognitive load using interruptions, "
        "task switching and session duration."
    )

    if filtered_df.empty:
        show_empty_message()

    else:

        load_counts = filtered_df[
            "cognitive_load"
        ].value_counts()

        low_load = int(
            (filtered_df["cognitive_load"] == "Low Estimated Load").sum()
        )

        moderate_load = int(
            (filtered_df["cognitive_load"] == "Moderate Estimated Load").sum()
        )

        high_load = int(
            (filtered_df["cognitive_load"] == "High Estimated Load").sum()
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            show_metric("Low Estimated Load", low_load)

        with c2:
            show_metric("Moderate Estimated Load", moderate_load)

        with c3:
            show_metric("High Estimated Load", high_load)

        st.divider()

        st.markdown("#### Cognitive Load Distribution")

        st.bar_chart(
            load_counts,
            color="#14B8A6"
        )

        left, right = st.columns(2)

        with left:

            st.markdown("#### Interruptions vs Task Switching")

            st.scatter_chart(
                filtered_df,
                x="switch_count",
                y="interruptions",
                color="cognitive_load"
            )

        with right:

            st.markdown("#### Average Session Duration by Load")

            average_duration = filtered_df.groupby(
                "cognitive_load"
            )["session_minutes"].mean()

            st.bar_chart(
                average_duration,
                color="#8B5CF6"
            )

        st.markdown("#### Cognitive Load Records")

        st.dataframe(
            filtered_df[
                [
                    "developer_id",
                    "session_minutes",
                    "switch_count",
                    "interruptions",
                    "cognitive_load"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Cognitive-load categories are illustrative, "
            "rule-based estimates and are not scientifically validated "
            "measurements of mental state."
        )


# =====================================================
# PAGE 4: ACTIVITY MONITORING
# =====================================================

elif page == "Activity Monitoring":

    show_page_title(
        "Developer Activity Monitoring",
        "Monitor coding sessions, breaks, task switches and interruptions."
    )

    if filtered_df.empty:
        show_empty_message()

    else:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            show_metric(
                "Coding Minutes",
                f"{filtered_df['session_minutes'].sum():.0f}"
            )

        with c2:
            show_metric(
                "Break Minutes",
                f"{filtered_df['break_minutes'].sum():.0f}"
            )

        with c3:
            show_metric(
                "Tasks Completed",
                int(filtered_df["tasks_completed"].sum())
            )

        with c4:
            show_metric(
                "Total Interruptions",
                int(filtered_df["interruptions"].sum())
            )

        st.divider()

        left, right = st.columns(2)

        with left:

            st.markdown("#### 💻 Session Duration")

            st.bar_chart(
                filtered_df["session_minutes"],
                color="#3B82F6"
            )

        with right:

            st.markdown("#### ☕ Break Duration")

            st.bar_chart(
                filtered_df["break_minutes"],
                color="#14B8A6"
            )

        st.markdown("#### Task Switching and Interruptions")

        st.line_chart(
            filtered_df[
                ["switch_count", "interruptions"]
            ],
            color=["#3B82F6", "#F59E0B"]
        )

        if "developer_id" in filtered_df.columns:

            st.markdown("#### Developer-wise Activity")

            developer_activity = filtered_df.groupby(
                "developer_id"
            ).agg(
                coding_minutes=("session_minutes", "sum"),
                break_minutes=("break_minutes", "sum"),
                tasks_completed=("tasks_completed", "sum")
            )

            st.bar_chart(
                developer_activity[
                    ["coding_minutes", "break_minutes"]
                ]
            )

        st.markdown("#### Activity Details")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# PAGE 5: TRENDS
# =====================================================

elif page == "Trends":

    show_page_title(
        "Developer Activity Trends",
        "Analyze daily developer activity and changes over time."
    )

    trend_data = filtered_df.dropna(
        subset=["date"]
    ).copy()

    if trend_data.empty:

        st.warning("No valid date records available.")

    else:

        trend_data["date"] = trend_data["date"].dt.date

        daily = trend_data.groupby("date").agg(
            total_sessions=("session_minutes", "count"),
            average_session=("session_minutes", "mean"),
            total_switches=("switch_count", "sum"),
            total_interruptions=("interruptions", "sum"),
            total_tasks=("tasks_completed", "sum")
        )

        st.markdown("#### 📈 Daily Session Count")

        st.line_chart(
            daily["total_sessions"],
            color="#3B82F6"
        )

        left, right = st.columns(2)

        with left:

            st.markdown("#### Average Session Duration")

            st.line_chart(
                daily["average_session"],
                color="#14B8A6"
            )

        with right:

            st.markdown("#### Daily Task Switching")

            st.bar_chart(
                daily["total_switches"],
                color="#8B5CF6"
            )

        left, right = st.columns(2)

        with left:

            st.markdown("#### Daily Interruption Trends")

            st.line_chart(
                daily["total_interruptions"],
                color="#F59E0B"
            )

        with right:

            st.markdown("#### Daily Tasks Completed")

            st.bar_chart(
                daily["total_tasks"],
                color="#06B6D4"
            )

        st.markdown("#### Trend Summary")

        st.dataframe(
            daily.round(2),
            use_container_width=True
        )


# =====================================================
# PAGE 6: REPORTS
# =====================================================

elif page == "Reports":

    show_page_title(
        "Developer Analytics Reports",
        "Generate and download reports from the selected activity data."
    )

    if filtered_df.empty:
        show_empty_message()

    else:

        report = {
            "Total Sessions": len(filtered_df),
            "Average Session Minutes": round(
                filtered_df["session_minutes"].mean(), 2
            ),
            "Total Task Switches": int(
                filtered_df["switch_count"].sum()
            ),
            "Total Interruptions": int(
                filtered_df["interruptions"].sum()
            ),
            "Total Tasks Completed": int(
                filtered_df["tasks_completed"].sum()
            ),
            "Total Coding Minutes": int(
                filtered_df["session_minutes"].sum()
            ),
            "Total Break Minutes": int(
                filtered_df["break_minutes"].sum()
            )
        }

        st.markdown("#### 📊 Report Summary")

        for start in range(0, len(report), 3):

            report_items = list(report.items())[start:start + 3]

            columns = st.columns(len(report_items))

            for column, (label, value) in zip(
                columns,
                report_items
            ):

                with column:
                    show_metric(label, value)

        st.divider()

        left, right = st.columns(2)

        with left:

            st.markdown("#### Focus Distribution")

            st.dataframe(
                filtered_df["focus_indicator"].value_counts()
                .rename_axis("Focus Category")
                .reset_index(name="Records"),
                use_container_width=True,
                hide_index=True
            )

        with right:

            st.markdown("#### Cognitive Load Distribution")

            st.dataframe(
                filtered_df["cognitive_load"].value_counts()
                .rename_axis("Load Category")
                .reset_index(name="Records"),
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        st.markdown("#### Download Reports")

        show_download_button(
            filtered_df,
            "cognistream_report.csv",
            "⬇️ Download CSV Report"
        )


# =====================================================
# PAGE 7: DATABASE
# =====================================================

elif page == "Database":

    show_page_title(
        "Developer Activity Database",
        "View, store and download developer activity records."
    )

    from src.database import (
        create_database,
        save_activity,
        get_all_activities
    )

    try:

        create_database()

        database_df = get_all_activities()

        st.markdown("#### Database Overview")

        if st.button(
            "💾 Save Dataset to Database",
            use_container_width=True
        ):

            if filtered_df.empty:

                st.warning(
                    "No records available for the selected date range."
                )

            elif database_df.empty:

                for _, row in filtered_df.iterrows():

                    save_activity({
                        "developer_id": row.get(
                            "developer_id",
                            "Unknown"
                        ),
                        "date": str(row.get("date", ""))[:10],
                        "session_minutes": float(
                            row["session_minutes"]
                        ),
                        "switch_count": int(
                            row["switch_count"]
                        ),
                        "interruptions": int(
                            row["interruptions"]
                        ),
                        "break_minutes": float(
                            row.get("break_minutes", 0)
                        ),
                        "tasks_completed": int(
                            row.get("tasks_completed", 0)
                        )
                    })

                st.success(
                    "Activity records saved successfully!"
                )

                st.rerun()

            else:

                st.info(
                    "Database already contains records. "
                    "Existing records were not duplicated."
                )

        database_df = get_all_activities()

        if not database_df.empty:

            col1, col2, col3 = st.columns(3)

            with col1:
                show_metric(
                    "Stored Sessions",
                    len(database_df)
                )

            with col2:
                show_metric(
                    "Total Task Switches",
                    int(database_df["switch_count"].sum())
                )

            with col3:
                show_metric(
                    "Total Interruptions",
                    int(database_df["interruptions"].sum())
                )

            st.divider()

            st.markdown("#### Stored Developer Records")

            st.dataframe(
                database_df,
                use_container_width=True,
                hide_index=True
            )

            show_download_button(
                database_df,
                "cognistream_database.csv",
                "⬇️ Download Database Records"
            )

        else:

            st.warning(
                "No database records available. "
                "Click Save Dataset to Database."
            )

    except Exception as error:

        st.error(
            f"Database operation failed: {error}"
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "CogniStream | Developer Flow-State & Cognitive Load Analytics"
)

st.caption(
    "Data source: data/sample_activity.csv"
)

st.caption(
    "Analytics are based on the activity records and "
    "project-defined classification rules."
)
