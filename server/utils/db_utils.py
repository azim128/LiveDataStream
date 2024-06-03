from config.db_config import get_db_connection


def add_value_to_db(value):
    conn = get_db_connection()
    conn.execute("INSERT INTO data_values (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()
