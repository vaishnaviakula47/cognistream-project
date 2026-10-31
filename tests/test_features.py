import unittest
from datetime import datetime, timedelta

from src.feature_calculator import (
calculate_session_duration,
calculate_switch_frequency,
calculate_activity_percentage,
)

class TestFeatureCalculations(unittest.TestCase):

def test_session_duration(self):
    start = datetime(2026, 10, 27, 10, 0)
    end = start + timedelta(minutes=30)
    self.assertEqual(
        calculate_session_duration(start, end), 30
    )

def test_switch_frequency(self):
    self.assertEqual(
        calculate_switch_frequency(4, 120), 2
    )

def test_zero_duration(self):
    self.assertEqual(
        calculate_switch_frequency(4, 0), 0
    )

def test_activity_percentage(self):
    self.assertEqual(
        calculate_activity_percentage(30, 60), 50
    )

def test_zero_total_time(self):
    self.assertEqual(
        calculate_activity_percentage(0, 0), 0
    )

if name == "main":
unittest.main()
