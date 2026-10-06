import sqlite3
from database import get_connection


# ============================================================
# GreenTill - Sample Supermarket Products
# ============================================================


products = [

    # -------------------- Vegetables --------------------

    (
        "P001",
        None,
        "Tomato",
        "Vegetables",
        "Kg",
        40.00,
        50.0,
        10.0,
        75,
        "Loose",
        None,
        "Active"
    ),

    (
        "P002",
        None,
        "Potato",
        "Vegetables",
        "Kg",
        35.00,
        60.0,
        10.0,
        70,
        "Loose",
        None,
        "Active"
    ),

    (
        "P003",
        None,
        "Onion",
        "Vegetables",
        "Kg",
        45.00,
        55.0,
        10.0,
        72,
        "Loose",
        None,
        "Active"
    ),

    # -------------------- Fruits --------------------

    (
        "P004",
        None,
        "Apple",
        "Fruits",
        "Kg",
        180.00,
        30.0,
        5.0,
        80,
        "Paper",
        None,
        "Active"
    ),

    (
        "P005",
        None,
        "Banana",
        "Fruits",
        "Dozen",
        60.00,
        40.0,
        8.0,
        78,
        "Loose",
        None,
        "Active"
    ),

    (
        "P006",
        None,
        "Orange",
        "Fruits",
        "Kg",
        120.00,
        25.0,
        5.0,
        76,
        "Loose",
        None,
        "Active"
    ),

    # -------------------- Dairy --------------------

    (
        "P007",
        "8901234500011",
        "Milk",
        "Dairy",
        "Liter",
        65.00,
        40.0,
        10.0,
        55,
        "Plastic",
        "2026-09-20",
        "Active"
    ),

    (
        "P008",
        "8901234500012",
        "Curd",
        "Dairy",
        "Pack",
        35.00,
        30.0,
        8.0,
        60,
        "Plastic",
        "2026-09-19",
        "Active"
    ),

    # -------------------- Grocery --------------------

    (
        "P009",
        "8901234500013",
        "Rice",
        "Grocery",
        "Kg",
        70.00,
        100.0,
        20.0,
        65,
        "Plastic",
        "2027-06-30",
        "Active"
    ),

    (
        "P010",
        "8901234500014",
        "Wheat Flour",
        "Grocery",
        "Kg",
        55.00,
        80.0,
        15.0,
        68,
        "Paper",
        "2027-03-31",
        "Active"
    ),

    # -------------------- Snacks --------------------

    (
        "P011",
        "8901234500015",
        "Biscuits",
        "Snacks",
        "Pack",
        30.00,
        75.0,
        15.0,
        50,
        "Plastic",
        "2027-01-15",
        "Active"
    ),

    # -------------------- Beverages --------------------

    (
        "P012",
        "8901234500016",
        "Fruit Juice",
        "Beverages",
        "Liter",
        110.00,
        35.0,
        8.0,
        52,
        "Plastic",
        "2027-02-28",
        "Active"
    ),

    # -------------------- Personal Care --------------------

    (
        "P013",
        "8901234500017",
        "Bath Soap",
        "Personal Care",
        "Piece",
        40.00,
        60.0,
        10.0,
        58,
        "Paper",
        None,
        "Active"
    ),

    # -------------------- Household --------------------

    (
        "P014",
        "8901234500018",
        "Dishwashing Liquid",
        "Household",
        "Liter",
        120.00,
        25.0,
        5.0,
        45,
        "Plastic",
        "2028-01-31",
        "Active"
    )
]


def seed_products():

    connection = get_connection()
    cursor = connection.cursor()

    added = 0
    skipped = 0

    for product in products:

        try:

            cursor.execute("""
                INSERT INTO products
                (
                    product_id,
                    barcode,
                    name,
                    category,
                    unit,
                    price,
                    stock,
                    reorder_level,
                    eco_score,
                    packaging_type,
                    expiry_date,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, product)

            added += 1

        except sqlite3.IntegrityError:
            skipped += 1

    connection.commit()
    connection.close()

    print(f"Products added: {added}")
    print(f"Products skipped: {skipped}")
    print("Product seeding completed successfully.")


if __name__ == "__main__":
    import sqlite3
    seed_products()