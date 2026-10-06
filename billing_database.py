import sqlite3
from database import get_connection


# ============================================================
# GreenTill - Billing Database
# Phase 6.1
# ============================================================


# ============================================================
# Bills Table
# ============================================================

def create_bills_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id TEXT PRIMARY KEY,
            employee_id TEXT NOT NULL,
            customer_id TEXT,
            bill_date TEXT NOT NULL DEFAULT CURRENT_DATE,
            bill_time TEXT NOT NULL DEFAULT CURRENT_TIME,
            subtotal REAL NOT NULL DEFAULT 0
                CHECK(subtotal >= 0),
            discount REAL NOT NULL DEFAULT 0
                CHECK(discount >= 0),
            tax REAL NOT NULL DEFAULT 0
                CHECK(tax >= 0),
            total_amount REAL NOT NULL DEFAULT 0
                CHECK(total_amount >= 0),
            payment_method TEXT,
            payment_status TEXT NOT NULL DEFAULT 'PENDING',
            eco_score INTEGER NOT NULL DEFAULT 0
                CHECK(eco_score >= 0 AND eco_score <= 100),
            eco_points INTEGER NOT NULL DEFAULT 0
                CHECK(eco_points >= 0),
            bill_status TEXT NOT NULL DEFAULT 'COMPLETED',

            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# Bill Items Table
# ============================================================

def create_bill_items_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            bill_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity REAL NOT NULL
                CHECK(quantity > 0),
            unit_price REAL NOT NULL
                CHECK(unit_price >= 0),
            eco_score INTEGER NOT NULL DEFAULT 0
                CHECK(eco_score >= 0 AND eco_score <= 100),
            item_total REAL NOT NULL
                CHECK(item_total >= 0),

            FOREIGN KEY (bill_id)
                REFERENCES bills(bill_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# Initialize Billing Database
# ============================================================

def initialize_billing_database():

    create_bills_table()
    create_bill_items_table()

    print("GreenTill billing tables created successfully.")


# ============================================================
# Run Directly
# ============================================================

if __name__ == "__main__":

    initialize_billing_database()