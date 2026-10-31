"""
CogniStream - Developer Activity Analysis
"""

import pandas as pd

def analyze_activity(df):
if df is None or df.empty:
return None

required_columns = [
    "session_minutes",
    "switch_count"
]

if not all(
    col in df.columns for col in required_columns
):
    raise ValueError("Required columns are missing")

result = {}

result["total_sessions"] = len(df)

result["average_session"] = round(
    df["session_minutes"].mean(), 2
)

result["total_switches"] = int(
    df["switch_count"].sum()
)

result["average_switches"] = round(
    df["switch_count"].mean(), 2
)

return result

if name == "main":
sample = pd.DataFrame({
"session_minutes": [30, 45, 60],
"switch_count": [2, 4, 5]
})

print(analyze_activity(sample))
