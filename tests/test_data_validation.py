import unittest
import pandas as pd

from src.data_validation import validate_activity_data

class TestDataValidation(unittest.TestCase):

def test_valid_dataset(self):
    df = pd.DataFrame({
        "session_minutes": [30, 45],
        "switch_count": [2, 4],
        "error_count": [1, 3]
    })

    result = validate_activity_data(df)

    self.assertEqual(len(result), 2)

def test_negative_values(self):
    df = pd.DataFrame({
        "session_minutes": [30, -5],
        "switch_count": [2, 4],
        "error_count": [1, 3]
    })

    result = validate_activity_data(df)

    self.assertEqual(len(result), 1)

def test_missing_columns(self):
    df = pd.DataFrame({
        "session_minutes": [30]
    })

    with self.assertRaises(ValueError):
        validate_activity_data(df)

def test_empty_dataset(self):
    result = validate_activity_data(
        pd.DataFrame()
    )

    self.assertIsNone(result)

if name == "main":
unittest.main()
