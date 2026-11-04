"""
Cognistream - Database Integration Module
"""

import sqlite3
import pandas as pd


DATABASE_NAME = "cognistream.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS developer_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            session_minutes REAL,
            switch_count INTEGER,
            error_count INTEGER,
            break_count INTEGER
        )
    """)

    connection.commit()
    connection.close()


def save_activity(data):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO developer_activity
        (timestamp, session_minutes, switch_count,
         error_count, break_count)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["session_minutes"],
        data["switch_count"],
        data["error_count"],
        data["break_count"]
    ))

    connection.commit()
    connection.close()


def get_all_activities():

    connection = sqlite3.connect(DATABASE_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM developer_activity",
        connection
    )

    connection.close()

    return df


if __name__ == "__main__":

    create_database()

    print("Cognistream database initialized.")

    records = get_all_activities()

    print(records)
