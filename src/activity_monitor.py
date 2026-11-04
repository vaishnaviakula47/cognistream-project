"""
Cognistream - Activity Monitor with Database Integration
"""

from datetime import datetime
from src.database import create_database, save_activity


class ActivityMonitor:

    def __init__(self):
        self.session_start = None
        self.task_switches = 0
        self.error_count = 0
        self.break_count = 0

        create_database()

    def start_session(self):

        self.session_start = datetime.now()

        self.task_switches = 0
        self.error_count = 0
        self.break_count = 0

        print("Developer session started.")

    def record_task_switch(self):
        self.task_switches += 1

    def record_error(self):
        self.error_count += 1

    def record_break(self):
        self.break_count += 1

    def end_session(self):

        if self.session_start is None:
            print("No active session.")
            return

        end_time = datetime.now()

        duration = (
            end_time - self.session_start
        ).total_seconds() / 60

        data = {
            "timestamp": self.session_start.isoformat(),
            "session_minutes": round(duration, 2),
            "switch_count": self.task_switches,
            "error_count": self.error_count,
            "break_count": self.break_count
        }

        save_activity(data)

        self.session_start = None

        print("Activity saved to database successfully.")


if __name__ == "__main__":

    monitor = ActivityMonitor()

    monitor.start_session()

    monitor.record_task_switch()
    monitor.record_error()
    monitor.record_break()

    monitor.end_session()
