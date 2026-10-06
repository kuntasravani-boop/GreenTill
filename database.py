import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "greentill.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def create_employees_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
        )
    """)

    connection.commit()
    connection.close()


def initialize_database():
    create_employees_table()
def authenticate_user(username, password):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT employee_id, name, username, role, status
        FROM employees
        WHERE username = ?
        AND password = ?
        """,
        (username, password)
    ).fetchone()

    connection.close()

    if user is None:
        return None

    if user["status"] != "Active":
        return None

    return user

if __name__ == "__main__":
    initialize_database()

    print("GreenTill database initialized successfully.")
    print(f"Database location: {DATABASE_FILE}")
