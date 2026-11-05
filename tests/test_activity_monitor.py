import unittest
from unittest.mock import patch, mock_open

from src.activity_monitor import ActivityMonitor


class TestActivityMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = ActivityMonitor()

    def test_start_session(self):
        self.monitor.start_session()

        self.assertIsNotNone(
            self.monitor.session_start
        )

    def test_task_switch(self):
        self.monitor.record_task_switch()
        self.monitor.record_task_switch()

        self.assertEqual(
            self.monitor.task_switches, 2
        )

    def test_error_count(self):
        self.monitor.record_error()

        self.assertEqual(
            self.monitor.error_count, 1
        )

    def test_break_count(self):
        self.monitor.record_break()

        self.assertEqual(
            self.monitor.break_count, 1
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_save_activity(self, mocked_file):

        self.monitor.start_session()
        self.monitor.end_session()

        mocked_file.assert_called_once()

        self.assertIsNone(
            self.monitor.session_start
        )

    @patch("builtins.open")
    def test_end_without_start(self, mocked_file):

        self.monitor.end_session()

        mocked_file.assert_not_called()


if __name__ == "__main__":
    unittest.main()
