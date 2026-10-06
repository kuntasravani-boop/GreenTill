from database import get_connection


def seed_users():
    connection = get_connection()
    cursor = connection.cursor()

    users = [
        (
            "EMP001",
            "GreenTill Admin",
            "admin",
            "admin123",
            "Admin",
            "Active"
        ),
        (
            "EMP002",
            "GreenTill Employee",
            "employee",
            "1234",
            "Employee",
            "Active"
        )
    ]

    for user in users:
        try:
            cursor.execute("""
                INSERT INTO employees
                (employee_id, name, username, password, role, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, user)

        except Exception:
            print(f"User '{user[2]}' already exists.")

    connection.commit()
    connection.close()

    print("Users added successfully.")


if __name__ == "__main__":
    seed_users()