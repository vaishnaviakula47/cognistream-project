"""
Cognistream - Developer Activity Monitor
"""

import csv
from datetime import datetime


class ActivityMonitor:

    def __init__(self):
        self.session_start = None
        self.task_switches = 0
        self.error_count = 0
        self.break_count = 0

    def start_session(self):
        self.session_start = datetime.now()
        print("Developer session started.")

    def record_task_switch(self):
        self.task_switches += 1
        print("Task switch recorded.")

    def record_error(self):
        self.error_count += 1
        print("Development error recorded.")

    def record_break(self):
        self.break_count += 1
        print("Break recorded.")

    def end_session(self):

        if self.session_start is None:
            print("No active session.")
            return

        end_time = datetime.now()

        duration = (
            end_time - self.session_start
        ).total_seconds() / 60

        data = {
            "timestamp": self.session_start,
            "session_minutes": round(duration, 2),
            "switch_count": self.task_switches,
            "error_count": self.error_count,
            "break_count": self.break_count
        }

        with open(
            "developer_activity.csv",
            "a",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=data.keys()
            )

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(data)

        print("Session completed.")
        print("Activity saved successfully.")


if __name__ == "__main__":

    monitor = ActivityMonitor()

    monitor.start_session()
    monitor.record_task_switch()
    monitor.record_error()
    monitor.record_break()
    monitor.end_session()
