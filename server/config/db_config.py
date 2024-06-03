import sqlite3


def get_db_connection():
    conn = sqlite3.connect("test.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS data_values (id INTEGER PRIMARY KEY, value TEXT)"
    )
    return conn
