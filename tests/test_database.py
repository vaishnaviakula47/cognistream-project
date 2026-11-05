import unittest
import tempfile
import os

import src.database as database


class TestDatabase(unittest.TestCase):

    def setUp(self):

        self.temp_file = tempfile.NamedTemporaryFile(
            suffix=".db",
            delete=False
        )

        self.temp_file.close()

        self.original_database = database.DATABASE_NAME

        database.DATABASE_NAME = self.temp_file.name

        database.create_database()

    def tearDown(self):

        database.DATABASE_NAME = self.original_database

        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_database_creation(self):

        self.assertTrue(
            os.path.exists(self.temp_file.name)
        )

    def test_save_activity(self):

        activity = {
            "timestamp": "2026-11-04 10:00:00",
            "session_minutes": 45,
            "switch_count": 3,
            "error_count": 1,
            "break_count": 2
        }

        database.save_activity(activity)

        result = database.get_all_activities()

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result.iloc[0]["switch_count"], 3
        )

    def test_empty_database(self):

        result = database.get_all_activities()

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
