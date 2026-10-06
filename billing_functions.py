import sqlite3
from datetime import datetime

from database import get_connection


# ============================================================
# GreenTill - Billing & Cart Functions
# Phase 6.2
# ============================================================


# ============================================================
# Database Connection Helper
# ============================================================

def get_billing_connection():

    connection = get_connection()

    # Enable SQLite foreign-key enforcement
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# Generate Bill ID
# ============================================================

def generate_bill_id():

    connection = None

    try:

        connection = get_billing_connection()

        last_bill = connection.execute(
            """
            SELECT bill_id
            FROM bills
            ORDER BY bill_id DESC
            LIMIT 1
            """
        ).fetchone()

        if not last_bill:

            return "B0001"

        last_id = last_bill["bill_id"]

        try:

            last_number = int(last_id[1:])
            new_number = last_number + 1

        except (ValueError, TypeError):

            new_number = 1

        return f"B{new_number:04d}"

    finally:

        if connection:
            connection.close()


# ============================================================
# Find Product By Product ID
# ============================================================

def get_product_by_id(product_id):

    connection = None

    try:

        connection = get_billing_connection()

        product = connection.execute(
            """
            SELECT
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
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        ).fetchone()

        return product

    finally:

        if connection:
            connection.close()


# ============================================================
# Find Product By Barcode
# ============================================================

def get_product_by_barcode(barcode):

    connection = None

    try:

        connection = get_billing_connection()

        product = connection.execute(
            """
            SELECT
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
            FROM products
            WHERE barcode = ?
            """,
            (barcode,)
        ).fetchone()

        return product

    finally:

        if connection:
            connection.close()


# ============================================================
# Search Products
# ============================================================

def search_products(search_text):

    connection = None

    try:

        connection = get_billing_connection()

        search_text = search_text.strip()

        if not search_text:

            return []

        pattern = f"%{search_text}%"

        products = connection.execute(
            """
            SELECT
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
            FROM products
            WHERE status = 'Active'
              AND (
                    product_id LIKE ?
                    OR barcode LIKE ?
                    OR name LIKE ?
              )
            ORDER BY name
            """,
            (
                pattern,
                pattern,
                pattern
            )
        ).fetchall()

        return products

    finally:

        if connection:
            connection.close()


# ============================================================
# Create Empty Cart
# ============================================================

def create_cart():

    return []


# ============================================================
# Add Product To Cart
# ============================================================

def add_to_cart(
    cart,
    product,
    quantity=1
):

    if quantity <= 0:

        raise ValueError(
            "Quantity must be greater than 0."
        )

    if product is None:

        raise ValueError(
            "Product not found."
        )

    if product["status"] != "Active":

        raise ValueError(
            "This product is inactive."
        )

    available_stock = float(
        product["stock"]
    )

    if quantity > available_stock:

        raise ValueError(
            f"Insufficient stock.\n"
            f"Available stock: {available_stock:g} "
            f"{product['unit']}"
        )

    product_id = product["product_id"]

    # --------------------------------------------------------
    # Check whether product is already in cart
    # --------------------------------------------------------

    for item in cart:

        if item["product_id"] == product_id:

            new_quantity = (
                item["quantity"] + quantity
            )

            if new_quantity > available_stock:

                raise ValueError(
                    f"Insufficient stock.\n"
                    f"Available stock: "
                    f"{available_stock:g} "
                    f"{product['unit']}"
                )

            item["quantity"] = new_quantity

            item["item_total"] = (
                new_quantity
                * item["unit_price"]
            )

            return cart

    # --------------------------------------------------------
    # Add New Cart Item
    # --------------------------------------------------------

    unit_price = float(
        product["price"]
    )

    item = {
        "product_id": product["product_id"],
        "barcode": product["barcode"],
        "name": product["name"],
        "category": product["category"],
        "unit": product["unit"],
        "quantity": float(quantity),
        "unit_price": unit_price,
        "eco_score": int(product["eco_score"]),
        "item_total": (
            float(quantity)
            * unit_price
        )
    }

    cart.append(item)

    return cart


# ============================================================
# Update Cart Quantity
# ============================================================

def update_cart_quantity(
    cart,
    product_id,
    new_quantity
):

    if new_quantity <= 0:

        raise ValueError(
            "Quantity must be greater than 0."
        )

    product = get_product_by_id(
        product_id
    )

    if not product:

        raise ValueError(
            "Product not found."
        )

    available_stock = float(
        product["stock"]
    )

    if new_quantity > available_stock:

        raise ValueError(
            f"Insufficient stock.\n"
            f"Available stock: "
            f"{available_stock:g} "
            f"{product['unit']}"
        )

    for item in cart:

        if item["product_id"] == product_id:

            item["quantity"] = float(
                new_quantity
            )

            item["item_total"] = (
                item["quantity"]
                * item["unit_price"]
            )

            return cart

    raise ValueError(
        "Product is not present in the cart."
    )


# ============================================================
# Remove Product From Cart
# ============================================================

def remove_from_cart(
    cart,
    product_id
):

    for item in cart:

        if item["product_id"] == product_id:

            cart.remove(item)

            return cart

    raise ValueError(
        "Product is not present in the cart."
    )


# ============================================================
# Clear Cart
# ============================================================

def clear_cart(cart):

    cart.clear()

    return cart


# ============================================================
# Calculate Subtotal
# ============================================================

def calculate_subtotal(cart):

    subtotal = 0.0

    for item in cart:

        subtotal += float(
            item["item_total"]
        )

    return round(
        subtotal,
        2
    )


# ============================================================
# Calculate Discount
# ============================================================

def calculate_discount(
    subtotal,
    discount=0
):

    discount = float(discount)

    if discount < 0:

        raise ValueError(
            "Discount cannot be negative."
        )

    if discount > subtotal:

        raise ValueError(
            "Discount cannot be greater than subtotal."
        )

    return round(
        discount,
        2
    )


# ============================================================
# Calculate Tax
# ============================================================

def calculate_tax(
    taxable_amount,
    tax_rate=0
):

    taxable_amount = float(
        taxable_amount
    )

    tax_rate = float(
        tax_rate
    )

    if taxable_amount < 0:

        raise ValueError(
            "Taxable amount cannot be negative."
        )

    if tax_rate < 0:

        raise ValueError(
            "Tax rate cannot be negative."
        )

    tax = (
        taxable_amount
        * tax_rate
        / 100
    )

    return round(
        tax,
        2
    )


# ============================================================
# Calculate Final Total
# ============================================================

def calculate_total(
    subtotal,
    discount=0,
    tax=0
):

    subtotal = float(subtotal)
    discount = float(discount)
    tax = float(tax)

    total = (
        subtotal
        - discount
        + tax
    )

    if total < 0:

        total = 0

    return round(
        total,
        2
    )


# ============================================================
# Calculate Bill Summary
# ============================================================

def calculate_bill_summary(
    cart,
    discount=0,
    tax_rate=0
):

    subtotal = calculate_subtotal(
        cart
    )

    discount_value = calculate_discount(
        subtotal,
        discount
    )

    taxable_amount = (
        subtotal
        - discount_value
    )

    tax_value = calculate_tax(
        taxable_amount,
        tax_rate
    )

    total = calculate_total(
        subtotal,
        discount_value,
        tax_value
    )

    return {
        "subtotal": subtotal,
        "discount": discount_value,
        "tax": tax_value,
        "total_amount": total
    }


# ============================================================
# Calculate Bill Eco Score
# ============================================================

def calculate_bill_eco_score(cart):

    if not cart:

        return 0

    total_value = 0.0
    weighted_score = 0.0

    for item in cart:

        item_total = float(
            item["item_total"]
        )

        eco_score = int(
            item["eco_score"]
        )

        total_value += item_total

        weighted_score += (
            item_total
            * eco_score
        )

    if total_value == 0:

        return 0

    score = (
        weighted_score
        / total_value
    )

    return round(score)


# ============================================================
# Validate Cart Stock
# ============================================================

def validate_cart_stock(cart):

    connection = None

    try:

        connection = get_billing_connection()

        for item in cart:

            product = connection.execute(
                """
                SELECT
                    product_id,
                    name,
                    unit,
                    stock,
                    status
                FROM products
                WHERE product_id = ?
                """,
                (item["product_id"],)
            ).fetchone()

            if not product:

                return False, (
                    f"Product '{item['product_id']}' "
                    f"no longer exists."
                )

            if product["status"] != "Active":

                return False, (
                    f"Product '{product['name']}' "
                    f"is no longer active."
                )

            current_stock = float(
                product["stock"]
            )

            requested_quantity = float(
                item["quantity"]
            )

            if requested_quantity > current_stock:

                return False, (
                    f"Insufficient stock for "
                    f"'{product['name']}'.\n"
                    f"Available: "
                    f"{current_stock:g} "
                    f"{product['unit']}\n"
                    f"Requested: "
                    f"{requested_quantity:g} "
                    f"{product['unit']}"
                )

        return True, "Stock available."

    finally:

        if connection:
            connection.close()


# ============================================================
# Complete Bill
# ============================================================

def complete_bill(
    employee_id,
    cart,
    payment_method,
    discount=0,
    tax_rate=0,
    customer_id=None
):

    if not employee_id:

        raise ValueError(
            "Employee ID is required."
        )

    if not cart:

        raise ValueError(
            "Cannot complete an empty cart."
        )

    if not payment_method:

        raise ValueError(
            "Payment method is required."
        )

    # --------------------------------------------------------
    # Calculate Bill
    # --------------------------------------------------------

    summary = calculate_bill_summary(
        cart,
        discount,
        tax_rate
    )

    eco_score = calculate_bill_eco_score(
        cart
    )

    # Eco points will be handled in the
    # Eco Dashboard phase.
    eco_points = 0

    # --------------------------------------------------------
    # Generate Bill ID
    # --------------------------------------------------------

    bill_id = generate_bill_id()

    connection = None

    try:

        connection = get_billing_connection()

        # ----------------------------------------------------
        # Verify Employee
        # ----------------------------------------------------

        employee = connection.execute(
            """
            SELECT employee_id, status
            FROM employees
            WHERE employee_id = ?
            """,
            (employee_id,)
        ).fetchone()

        if not employee:

            raise ValueError(
                "Employee account not found."
            )

        if employee["status"] != "Active":

            raise ValueError(
                "Employee account is inactive."
            )

        # ----------------------------------------------------
        # Begin Transaction
        # ----------------------------------------------------

        connection.execute(
            "BEGIN"
        )

        # ----------------------------------------------------
        # Re-check Stock
        #
        # This is important because stock may have changed
        # after the cart was created.
        # ----------------------------------------------------

        for item in cart:

            product = connection.execute(
                """
                SELECT
                    product_id,
                    name,
                    unit,
                    stock,
                    status,
                    price,
                    eco_score
                FROM products
                WHERE product_id = ?
                """,
                (item["product_id"],)
            ).fetchone()

            if not product:

                raise ValueError(
                    f"Product '{item['product_id']}' "
                    f"was not found."
                )

            if product["status"] != "Active":

                raise ValueError(
                    f"Product '{product['name']}' "
                    f"is inactive."
                )

            current_stock = float(
                product["stock"]
            )

            requested_quantity = float(
                item["quantity"]
            )

            if requested_quantity > current_stock:

                raise ValueError(
                    f"Insufficient stock for "
                    f"'{product['name']}'.\n"
                    f"Available: "
                    f"{current_stock:g} "
                    f"{product['unit']}"
                )

        # ----------------------------------------------------
        # Insert Bill
        # ----------------------------------------------------

        connection.execute(
            """
            INSERT INTO bills
            (
                bill_id,
                employee_id,
                customer_id,
                subtotal,
                discount,
                tax,
                total_amount,
                payment_method,
                payment_status,
                eco_score,
                eco_points,
                bill_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                bill_id,
                employee_id,
                customer_id,
                summary["subtotal"],
                summary["discount"],
                summary["tax"],
                summary["total_amount"],
                payment_method,
                "PAID",
                eco_score,
                eco_points,
                "COMPLETED"
            )
        )

        # ----------------------------------------------------
        # Insert Bill Items + Reduce Stock
        # ----------------------------------------------------

        for item in cart:

            product = connection.execute(
                """
                SELECT stock
                FROM products
                WHERE product_id = ?
                """,
                (item["product_id"],)
            ).fetchone()

            stock_before = float(
                product["stock"]
            )

            quantity = float(
                item["quantity"]
            )

            stock_after = (
                stock_before
                - quantity
            )

            # Insert bill item
            connection.execute(
                """
                INSERT INTO bill_items
                (
                    bill_id,
                    product_id,
                    quantity,
                    unit_price,
                    eco_score,
                    item_total
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    bill_id,
                    item["product_id"],
                    quantity,
                    item["unit_price"],
                    item["eco_score"],
                    item["item_total"]
                )
            )

            # Reduce product stock
            connection.execute(
                """
                UPDATE products
                SET stock = ?
                WHERE product_id = ?
                """,
                (
                    stock_after,
                    item["product_id"]
                )
            )

            # Record inventory transaction
            connection.execute(
                """
                INSERT INTO inventory_transactions
                (
                    product_id,
                    transaction_type,
                    quantity,
                    stock_before,
                    stock_after,
                    reason,
                    employee_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["product_id"],
                    "SALE",
                    quantity,
                    stock_before,
                    stock_after,
                    f"Sale - Bill {bill_id}",
                    employee_id
                )
            )

        # ----------------------------------------------------
        # Commit Everything Together
        # ----------------------------------------------------

        connection.commit()

        return {
            "bill_id": bill_id,
            "employee_id": employee_id,
            "customer_id": customer_id,
            "subtotal": summary["subtotal"],
            "discount": summary["discount"],
            "tax": summary["tax"],
            "total_amount": summary["total_amount"],
            "payment_method": payment_method,
            "payment_status": "PAID",
            "eco_score": eco_score,
            "eco_points": eco_points,
            "bill_status": "COMPLETED"
        }

    except Exception:

        if connection:

            connection.rollback()

        raise

    finally:

        if connection:
            connection.close()


# ============================================================
# Get Bill
# ============================================================

def get_bill(bill_id):

    connection = None

    try:

        connection = get_billing_connection()

        bill = connection.execute(
            """
            SELECT
                bill_id,
                employee_id,
                customer_id,
                bill_date,
                bill_time,
                subtotal,
                discount,
                tax,
                total_amount,
                payment_method,
                payment_status,
                eco_score,
                eco_points,
                bill_status
            FROM bills
            WHERE bill_id = ?
            """,
            (bill_id,)
        ).fetchone()

        return bill

    finally:

        if connection:
            connection.close()


# ============================================================
# Get Bill Items
# ============================================================

def get_bill_items(bill_id):

    connection = None

    try:

        connection = get_billing_connection()

        items = connection.execute(
            """
            SELECT
                bi.bill_item_id,
                bi.bill_id,
                bi.product_id,
                p.name AS product_name,
                p.unit,
                bi.quantity,
                bi.unit_price,
                bi.eco_score,
                bi.item_total
            FROM bill_items bi
            LEFT JOIN products p
                ON bi.product_id = p.product_id
            WHERE bi.bill_id = ?
            ORDER BY bi.bill_item_id
            """,
            (bill_id,)
        ).fetchall()

        return items

    finally:

        if connection:
            connection.close()


# ============================================================
# Test Functions
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("GreenTill Billing Functions Test")
    print("=" * 55)

    # Test bill ID
    bill_id = generate_bill_id()

    print(f"\nNext Bill ID: {bill_id}")

    # Test product search
    products = search_products("Tomato")

    print(
        f"Products found for 'Tomato': "
        f"{len(products)}"
    )

    if products:

        product = products[0]

        print("\nProduct Found:")
        print(
            f"  ID: {product['product_id']}"
        )
        print(
            f"  Name: {product['name']}"
        )
        print(
            f"  Unit: {product['unit']}"
        )
        print(
            f"  Price: ₹{product['price']:.2f}"
        )
        print(
            f"  Stock: {float(product['stock']):g}"
        )

        # Test cart
        cart = create_cart()

        add_to_cart(
            cart,
            product,
            1
        )

        print(
            f"\nCart Items: {len(cart)}"
        )

        summary = calculate_bill_summary(
            cart
        )

        print(
            f"Subtotal: ₹{summary['subtotal']:.2f}"
        )

        print(
            f"Discount: ₹{summary['discount']:.2f}"
        )

        print(
            f"Tax: ₹{summary['tax']:.2f}"
        )

        print(
            f"Total: ₹{summary['total_amount']:.2f}"
        )

        print(
            f"Eco Score: "
            f"{calculate_bill_eco_score(cart)}/100"
        )

    print("\nBilling functions are working.")
    print("=" * 55)