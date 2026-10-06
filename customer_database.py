from database import get_connection


# ============================================================
# GREEN TILL - CUSTOMER DATABASE
# ============================================================


def create_customers_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (

            customer_id TEXT PRIMARY KEY,

            name TEXT NOT NULL,

            phone TEXT UNIQUE,

            email TEXT,

            address TEXT,

            created_date TEXT NOT NULL DEFAULT CURRENT_DATE,

            status TEXT NOT NULL DEFAULT 'Active'

        )
    """)

    connection.commit()
    connection.close()


def initialize_customer_database():

    create_customers_table()

    print(
        "GreenTill customer table created successfully."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    initialize_customer_database()