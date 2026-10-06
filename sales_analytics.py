from database import get_connection


def get_today_sales():
    """
    Return today's completed sales amount.
    """

    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT COALESCE(SUM(total_amount), 0) AS total_sales
            FROM bills
            WHERE bill_date = CURRENT_DATE
            AND bill_status = 'COMPLETED'
            AND payment_status = 'PAID'
            """
        ).fetchone()

        return float(result["total_sales"])

    finally:
        connection.close()


def get_today_bill_count():
    """
    Return the number of completed bills today.
    """

    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT COUNT(*) AS bill_count
            FROM bills
            WHERE bill_date = CURRENT_DATE
            AND bill_status = 'COMPLETED'
            AND payment_status = 'PAID'
            """
        ).fetchone()

        return int(result["bill_count"])

    finally:
        connection.close()


def get_today_items_sold():
    """
    Return total quantity of products sold today.
    """

    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT COALESCE(SUM(bi.quantity), 0) AS items_sold
            FROM bill_items bi
            JOIN bills b
                ON bi.bill_id = b.bill_id
            WHERE b.bill_date = CURRENT_DATE
            AND b.bill_status = 'COMPLETED'
            AND b.payment_status = 'PAID'
            """
        ).fetchone()

        return float(result["items_sold"])

    finally:
        connection.close()


def get_today_customers_served():
    """
    Return number of unique customers served today.

    Guest bills are not counted as registered customers.
    """

    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT COUNT(DISTINCT customer_id) AS customers_served
            FROM bills
            WHERE bill_date = CURRENT_DATE
            AND bill_status = 'COMPLETED'
            AND payment_status = 'PAID'
            AND customer_id IS NOT NULL
            """
        ).fetchone()

        return int(result["customers_served"])

    finally:
        connection.close()


def get_today_payment_sales():
    """
    Return today's sales grouped by payment method.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                payment_method,
                COALESCE(SUM(total_amount), 0) AS amount
            FROM bills
            WHERE bill_date = CURRENT_DATE
            AND bill_status = 'COMPLETED'
            AND payment_status = 'PAID'
            GROUP BY payment_method
            """
        ).fetchall()

        payment_sales = {
            "Cash": 0.0,
            "UPI": 0.0,
            "Card": 0.0
        }

        for row in rows:
            method = row["payment_method"]

            if method in payment_sales:
                payment_sales[method] = float(row["amount"])

        return payment_sales

    finally:
        connection.close()


def get_today_sales_by_category():
    """
    Return today's sales grouped by product category.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                p.category,
                COALESCE(SUM(bi.item_total), 0) AS sales
            FROM bill_items bi
            JOIN bills b
                ON bi.bill_id = b.bill_id
            JOIN products p
                ON bi.product_id = p.product_id
            WHERE b.bill_date = CURRENT_DATE
            AND b.bill_status = 'COMPLETED'
            AND b.payment_status = 'PAID'
            GROUP BY p.category
            ORDER BY sales DESC
            """
        ).fetchall()

        return [
            {
                "category": row["category"],
                "sales": float(row["sales"])
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_today_employee_sales():
    """
    Return today's sales grouped by employee.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                b.employee_id,
                e.name AS employee_name,
                COUNT(b.bill_id) AS bill_count,
                COALESCE(SUM(b.total_amount), 0) AS total_sales
            FROM bills b
            LEFT JOIN employees e
                ON b.employee_id = e.employee_id
            WHERE b.bill_date = CURRENT_DATE
            AND b.bill_status = 'COMPLETED'
            AND b.payment_status = 'PAID'
            GROUP BY b.employee_id, e.name
            ORDER BY total_sales DESC
            """
        ).fetchall()

        return [
            {
                "employee_id": row["employee_id"],
                "employee_name": row["employee_name"],
                "bill_count": int(row["bill_count"]),
                "total_sales": float(row["total_sales"])
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_recent_bills(limit=10):
    """
    Return recent completed bills.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                b.bill_id,
                b.bill_date,
                b.bill_time,
                b.employee_id,
                e.name AS employee_name,
                b.customer_id,
                c.name AS customer_name,
                b.total_amount,
                b.payment_method
            FROM bills b
            LEFT JOIN employees e
                ON b.employee_id = e.employee_id
            LEFT JOIN customers c
                ON b.customer_id = c.customer_id
            WHERE b.bill_status = 'COMPLETED'
            AND b.payment_status = 'PAID'
            ORDER BY
                b.bill_date DESC,
                b.bill_time DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        return [
            {
                "bill_id": row["bill_id"],
                "bill_date": row["bill_date"],
                "bill_time": row["bill_time"],
                "employee_id": row["employee_id"],
                "employee_name": row["employee_name"],
                "customer_id": row["customer_id"],
                "customer_name": row["customer_name"],
                "total_amount": float(row["total_amount"]),
                "payment_method": row["payment_method"]
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_today_sales_summary():
    """
    Return all important sales statistics for today.
    """

    return {
        "total_sales": get_today_sales(),
        "bill_count": get_today_bill_count(),
        "items_sold": get_today_items_sold(),
        "customers_served": get_today_customers_served(),
        "payment_sales": get_today_payment_sales(),
        "category_sales": get_today_sales_by_category(),
        "employee_sales": get_today_employee_sales(),
        "recent_bills": get_recent_bills()
    }


def print_today_sales_report():
    """
    Print a simple sales report for testing.
    """

    summary = get_today_sales_summary()

    print()
    print("=" * 50)
    print("       GreenTill Sales Analytics")
    print("=" * 50)

    print()
    print("Today's Sales       : ₹{:.2f}".format(
        summary["total_sales"]
    ))

    print("Today's Bills       : {}".format(
        summary["bill_count"]
    ))

    print("Items Sold          : {}".format(
        summary["items_sold"]
    ))

    print("Customers Served    : {}".format(
        summary["customers_served"]
    ))

    print()
    print("-" * 50)
    print("Payment Methods")
    print("-" * 50)

    payment_sales = summary["payment_sales"]

    print("Cash                : ₹{:.2f}".format(
        payment_sales["Cash"]
    ))

    print("UPI                 : ₹{:.2f}".format(
        payment_sales["UPI"]
    ))

    print("Card                : ₹{:.2f}".format(
        payment_sales["Card"]
    ))

    print()
    print("-" * 50)
    print("Sales by Category")
    print("-" * 50)

    if summary["category_sales"]:
        for item in summary["category_sales"]:
            print(
                "{:<20}: ₹{:.2f}".format(
                    item["category"],
                    item["sales"]
                )
            )
    else:
        print("No sales recorded today.")

    print()
    print("-" * 50)
    print("Employee Sales")
    print("-" * 50)

    if summary["employee_sales"]:
        for employee in summary["employee_sales"]:
            print(
                "{} ({}) : ₹{:.2f} | Bills: {}".format(
                    employee["employee_name"],
                    employee["employee_id"],
                    employee["total_sales"],
                    employee["bill_count"]
                )
            )
    else:
        print("No employee sales recorded today.")

    print()
    print("-" * 50)
    print("Recent Bills")
    print("-" * 50)

    if summary["recent_bills"]:
        for bill in summary["recent_bills"]:
            print(
                "{} | {} | ₹{:.2f} | {}".format(
                    bill["bill_id"],
                    bill["bill_date"],
                    bill["total_amount"],
                    bill["payment_method"]
                )
            )
    else:
        print("No completed bills found.")

    print("=" * 50)
    print()


if __name__ == "__main__":
    print_today_sales_report()