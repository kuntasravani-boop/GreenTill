from customer_functions import (
    get_customer_by_phone,
    get_customer_history
)

phone = input("Enter customer phone number: ").strip()

customer = get_customer_by_phone(phone)

if customer is None:
    print()
    print("No customer found with this phone number.")

else:
    print()
    print("========================================")
    print("CUSTOMER FOUND")
    print("========================================")
    print("Customer ID:", customer["customer_id"])
    print("Name:", customer["name"])

    history = get_customer_history(
        customer["customer_id"]
    )

    print()
    print("========================================")
    print("PURCHASE HISTORY")
    print("========================================")

    if not history:
        print("No completed purchases found.")

    else:
        total_spent = 0

        for bill in history:
            print(
                f"{bill['bill_id']} | "
                f"{bill['bill_date']} | "
                f"{bill['bill_time']} | "
                f"₹{bill['total_amount']:.2f} | "
                f"{bill['payment_method']}"
            )

            total_spent += bill["total_amount"]

        print()
        print("Total Bills:", len(history))
        print(f"Total Purchases: ₹{total_spent:.2f}")