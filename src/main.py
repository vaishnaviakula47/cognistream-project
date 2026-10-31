"""
Cognistream - Main Application
"""

from data_processor import load_activity_data, clean_activity_data


def run_pipeline(file_path):
    """Load and clean activity data."""
    data = load_activity_data(file_path)

    if data is None:
        return None

    cleaned_data = clean_activity_data(data)

    if cleaned_data is None or cleaned_data.empty:
        print("No usable activity records found.")
        return None

    print("Data processing completed.")
    print("Records:", len(cleaned_data))
    print("Columns:", list(cleaned_data.columns))

    return cleaned_data


if __name__ == "__main__":
    print("Cognistream pipeline initialized.")
    print("Call run_pipeline() with a valid CSV file path.")
