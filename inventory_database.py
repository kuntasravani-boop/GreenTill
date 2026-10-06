import sqlite3
from database import get_connection


# ============================================================
# GreenTill - Inventory Database
# Phase 5.1
# ============================================================


def create_inventory_transactions_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_transactions (

            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_id TEXT NOT NULL,

            transaction_type TEXT NOT NULL,

            quantity REAL NOT NULL
                CHECK(quantity > 0),

            stock_before REAL NOT NULL
                CHECK(stock_before >= 0),

            stock_after REAL NOT NULL
                CHECK(stock_after >= 0),

            reason TEXT,

            employee_id TEXT,

            transaction_date TEXT NOT NULL DEFAULT CURRENT_DATE,

            transaction_time TEXT NOT NULL DEFAULT CURRENT_TIME,

            FOREIGN KEY (product_id)
                REFERENCES products(product_id),

            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)

        )
    """)

    connection.commit()
    connection.close()


def initialize_inventory_database():

    create_inventory_transactions_table()

    print(
        "GreenTill inventory transaction table "
        "created successfully."
    )


if __name__ == "__main__":

    initialize_inventory_database()