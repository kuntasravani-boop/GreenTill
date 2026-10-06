from database import get_connection


def find_or_create_customer(name, phone):
    """
    Customer details are optional.

    Cases:
    1. Name + phone -> find existing customer or create new one
    2. Name only    -> create customer with no phone
    3. Phone only   -> create/find customer using phone
    4. Both empty   -> guest transaction, return None
    """

    name = (name or "").strip()
    phone = (phone or "").strip()

    # ------------------------------------------------
    # NO CUSTOMER DETAILS
    # ------------------------------------------------

    if not name and not phone:
        return None

    connection = get_connection()

    try:

        # ------------------------------------------------
        # NAME + PHONE
        # ------------------------------------------------

        if name and phone:

            customer = connection.execute(
                """
                SELECT customer_id
                FROM customers
                WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
                AND phone = ?
                AND status = 'Active'
                """,
                (name, phone)
            ).fetchone()

            if customer:
                return customer["customer_id"]

        # ------------------------------------------------
        # PHONE ONLY
        # ------------------------------------------------

        elif phone and not name:

            customer = connection.execute(
                """
                SELECT customer_id
                FROM customers
                WHERE phone = ?
                AND status = 'Active'
                """,
                (phone,)
            ).fetchone()

            if customer:
                return customer["customer_id"]

            name = "Guest"

        # ------------------------------------------------
        # NAME ONLY
        # ------------------------------------------------

        elif name and not phone:

            # No phone available, so create a new customer
            # using the entered name.
            phone = None

        # ------------------------------------------------
        # GENERATE CUSTOMER ID
        # ------------------------------------------------

        last_customer = connection.execute(
            """
            SELECT customer_id
            FROM customers
            ORDER BY customer_id DESC
            LIMIT 1
            """
        ).fetchone()

        if last_customer is None:

            customer_id = "C0001"

        else:

            last_id = last_customer["customer_id"]

            try:
                number = int(last_id[1:])
                customer_id = f"C{number + 1:04d}"

            except (ValueError, TypeError):

                customer_id = "C0001"

        # ------------------------------------------------
        # CREATE CUSTOMER
        # ------------------------------------------------

        connection.execute(
            """
            INSERT INTO customers
            (
                customer_id,
                name,
                phone
            )
            VALUES (?, ?, ?)
            """,
            (
                customer_id,
                name,
                phone
            )
        )

        connection.commit()

        return customer_id

    except Exception:

        connection.rollback()
        raise

    finally:

        connection.close()
def get_customer_by_phone(phone):
    """
    Find an active customer using their phone number.

    This function only searches.
    It does NOT create a new customer.
    """

    phone = (phone or "").strip()

    if not phone:
        return None

    connection = get_connection()

    try:
        customer = connection.execute(
            """
            SELECT
                customer_id,
                name,
                phone
            FROM customers
            WHERE phone = ?
            AND status = 'Active'
            """,
            (phone,)
        ).fetchone()

        return customer

    finally:
        connection.close()


def get_customer_history(customer_id):
    """
    Return completed bills belonging to a customer.

    History is ordered from newest bill to oldest bill.
    """

    if not customer_id:
        return []

    connection = get_connection()

    try:
        history = connection.execute(
            """
            SELECT
                bill_id,
                bill_date,
                bill_time,
                total_amount,
                payment_method,
                payment_status
            FROM bills
            WHERE customer_id = ?
            AND bill_status = 'COMPLETED'
            ORDER BY
                bill_date DESC,
                bill_time DESC
            """,
            (customer_id,)
        ).fetchall()

        return history

    finally:
        connection.close()

if __name__ == "__main__":

    print(
        "GreenTill customer matching functions loaded successfully."
    )