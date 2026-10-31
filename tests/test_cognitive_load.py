import unittest

from src.cognitive_load import estimate_cognitive_load

class TestCognitiveLoad(unittest.TestCase):

def test_low_load(self):
    self.assertEqual(
        estimate_cognitive_load(2, 1, 30),
        "Low Estimated Load"
    )

def test_moderate_load(self):
    self.assertEqual(
        estimate_cognitive_load(6, 5, 90),
        "Moderate Estimated Load"
    )

def test_high_load(self):
    self.assertEqual(
        estimate_cognitive_load(12, 12, 150),
        "High Estimated Load"
    )

def test_invalid_input(self):
    self.assertEqual(
        estimate_cognitive_load(-1, 2, 30),
        "Invalid Input"
    )

if name == "main":
unittest.main()
