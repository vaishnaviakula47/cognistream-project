"""
CogniStream - Database Integration Module
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
            developer_id TEXT,
            date TEXT,
            session_minutes REAL,
            switch_count INTEGER,
            interruptions INTEGER,
            break_minutes REAL,
            tasks_completed INTEGER
        )
    """)

    # Add missing columns if an older database already exists.
    existing_columns = {
        row[1] for row in cursor.execute(
            "PRAGMA table_info(developer_activity)"
        ).fetchall()
    }

    new_columns = {
        "developer_id": "TEXT",
        "date": "TEXT",
        "interruptions": "INTEGER DEFAULT 0",
        "break_minutes": "REAL DEFAULT 0",
        "tasks_completed": "INTEGER DEFAULT 0"
    }

    for column, data_type in new_columns.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE developer_activity "
                f"ADD COLUMN {column} {data_type}"
            )

    connection.commit()
    connection.close()


def save_activity(data):

    create_database()

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO developer_activity (
            developer_id,
            date,
            session_minutes,
            switch_count,
            interruptions,
            break_minutes,
            tasks_completed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("developer_id"),
        str(data.get("date", "")),
        data["session_minutes"],
        data["switch_count"],
        data.get("interruptions", 0),
        data.get("break_minutes", 0),
        data.get("tasks_completed", 0)
    ))

    connection.commit()
    connection.close()


def get_all_activities():

    create_database()

    connection = sqlite3.connect(DATABASE_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM developer_activity",
        connection
    )

    connection.close()

    return df


if __name__ == "__main__":

    create_database()

    print("CogniStream database initialized.")

    print(get_all_activities())
