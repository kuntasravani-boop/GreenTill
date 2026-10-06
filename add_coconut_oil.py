from database import get_connection


connection = get_connection()

connection.execute(
    """
    INSERT INTO products (
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
    """,
    (
        "P015",
        "89002940",
        "Coconut Oil",
        "Grocery",
        "Liter",
        180.0,
        20.0,
        5.0,
        60,
        "Bottle",
        None,
        "Active"
    )
)

connection.commit()
connection.close()

print("Coconut Oil added successfully.")