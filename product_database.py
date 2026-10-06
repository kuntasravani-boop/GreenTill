import sqlite3
from database import get_connection


# ============================================================
# GreenTill - Product Database
# Phase 4.1
# ============================================================


def create_products_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (

            product_id TEXT PRIMARY KEY,

            barcode TEXT UNIQUE,

            name TEXT NOT NULL,

            category TEXT NOT NULL,

            unit TEXT NOT NULL,

            price REAL NOT NULL CHECK(price >= 0),

            stock REAL NOT NULL DEFAULT 0
                CHECK(stock >= 0),

            reorder_level REAL NOT NULL DEFAULT 5
                CHECK(reorder_level >= 0),

            eco_score INTEGER NOT NULL DEFAULT 0
                CHECK(eco_score >= 0 AND eco_score <= 100),

            packaging_type TEXT DEFAULT 'Not Specified',

            expiry_date TEXT,

            status TEXT NOT NULL DEFAULT 'Active'

        )
    """)

    connection.commit()
    connection.close()


def initialize_product_database():

    create_products_table()

    print("GreenTill product table created successfully.")


if __name__ == "__main__":

    initialize_product_database()