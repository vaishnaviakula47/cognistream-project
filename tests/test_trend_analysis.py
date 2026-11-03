import unittest
import pandas as pd

from src.trend_analysis import analyze_activity_trends

class TestTrendAnalysis(unittest.TestCase):

def setUp(self):

    self.df = pd.DataFrame({
        "timestamp": [
            "2026-11-01 10:00:00",
            "2026-11-01 11:00:00",
            "2026-11-02 10:00:00"
        ],
        "session_minutes": [30, 60, 45],
        "switch_count": [2, 4, 3]
    })

def test_trend_output(self):

    result = analyze_activity_trends(self.df)

    self.assertEqual(len(result), 2)

def test_total_sessions(self):

    result = analyze_activity_trends(self.df)

    self.assertEqual(
        result["total_sessions"].tolist(),
        [2, 1]
    )

def test_average_session(self):

    result = analyze_activity_trends(self.df)

    self.assertEqual(
        result["average_session"].tolist(),
        [45.0, 45.0]
    )

def test_empty_dataset(self):

    result = analyze_activity_trends(
        pd.DataFrame()
    )

    self.assertIsNone(result)

if name == "main":
unittest.main()
