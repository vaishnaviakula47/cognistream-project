import unittest

from src.flow_state import classify_focus

class TestFlowState(unittest.TestCase):

def test_high_focus_indicator(self):
    self.assertEqual(
        classify_focus(30, 2),
        "High Focus Indicator",
    )

def test_moderate_focus_indicator(self):
    self.assertEqual(
        classify_focus(15, 5),
        "Moderate Focus Indicator",
    )

def test_low_focus_indicator(self):
    self.assertEqual(
        classify_focus(5, 10),
        "Low Focus Indicator",
    )

def test_negative_session_duration(self):
    self.assertEqual(
        classify_focus(-5, 2),
        "Invalid Input",
    )

def test_negative_switch_frequency(self):
    self.assertEqual(
        classify_focus(30, -1),
        "Invalid Input",
    )

if name == "main":
unittest.main()
