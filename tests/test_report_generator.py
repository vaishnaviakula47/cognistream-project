import unittest
import pandas as pd

from src.report_generator import generate_activity_report

class TestReportGenerator(unittest.TestCase):

def setUp(self):
    self.df = pd.DataFrame({
        "session_minutes": [30, 60],
        "switch_count": [2, 4],
        "error_count": [1, 3],
        "focus_indicator": [
            "High Focus Indicator",
            "Moderate Focus Indicator"
        ],
        "cognitive_load": [
            "Low Estimated Load",
            "Moderate Estimated Load"
        ]
    })

def test_total_sessions(self):
    report = generate_activity_report(self.df)

    self.assertEqual(
        report["total_sessions"], 2
    )

def test_average_session(self):
    report = generate_activity_report(self.df)

    self.assertEqual(
        report["average_session_minutes"], 45
    )

def test_total_switches(self):
    report = generate_activity_report(self.df)

    self.assertEqual(
        report["total_task_switches"], 6
    )

def test_empty_dataset(self):
    report = generate_activity_report(
        pd.DataFrame()
    )

    self.assertIsNone(report)

if name == "main":
unittest.main()
