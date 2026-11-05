"""CogniStream - Feature Calculator
"""

def calculate_session_duration(start_time, end_time):
"""Calculate session duration in minutes."""
duration = (end_time - start_time).total_seconds() / 60

if duration < 0:
    raise ValueError("End time cannot be earlier than start time.")

return duration

def calculate_switch_frequency(switch_count, duration_minutes):
"""Calculate task switches per hour."""
if switch_count < 0:
raise ValueError("Switch count cannot be negative.")

if duration_minutes < 0:
    raise ValueError("Duration cannot be negative.")

if duration_minutes == 0:
    return 0

return switch_count / (duration_minutes / 60)

def calculate_activity_percentage(active_minutes, total_minutes):
"""Calculate active time as a percentage."""
if active_minutes < 0 or total_minutes < 0:
raise ValueError("Durations cannot be negative.")

if active_minutes > total_minutes:
    raise ValueError("Active time cannot exceed total time.")

if total_minutes == 0:
    return 0

return (active_minutes / total_minutes) * 100
