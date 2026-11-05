"""
CogniStream - Activity Monitor with Database Integration
"""

from datetime import datetime

from src.database import create_database, save_activity


class ActivityMonitor:

    def __init__(self, developer_id="D001"):

        self.developer_id = developer_id
        self.session_start = None
        self.task_switches = 0
        self.interruptions = 0
        self.break_minutes = 0
        self.tasks_completed = 0

        create_database()

    def start_session(self):

        self.session_start = datetime.now()

        self.task_switches = 0
        self.interruptions = 0
        self.break_minutes = 0
        self.tasks_completed = 0

        print("Developer session started.")

    def record_task_switch(self):
        self.task_switches += 1

    def record_interruption(self):
        self.interruptions += 1

    def record_break(self, minutes):
        if minutes < 0:
            raise ValueError("Break minutes cannot be negative.")

        self.break_minutes += minutes

    def record_task_completed(self):
        self.tasks_completed += 1

    def end_session(self):

        if self.session_start is None:
            print("No active session.")
            return

        end_time = datetime.now()

        duration = (
            end_time - self.session_start
        ).total_seconds() / 60

        data = {
            "developer_id": self.developer_id,
            "date": self.session_start.date().isoformat(),
            "session_minutes": round(duration, 2),
            "switch_count": self.task_switches,
            "interruptions": self.interruptions,
            "break_minutes": self.break_minutes,
            "tasks_completed": self.tasks_completed
        }

        save_activity(data)

        self.session_start = None

        print("Activity saved to database successfully.")


if __name__ == "__main__":

    monitor = ActivityMonitor("D001")

    monitor.start_session()

    monitor.record_task_switch()
    monitor.record_interruption()
    monitor.record_break(10)
    monitor.record_task_completed()

    monitor.end_session()
