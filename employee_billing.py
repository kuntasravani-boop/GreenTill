import customtkinter as ctk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
from urllib.parse import quote
from customer_functions import (
    find_or_create_customer,
    get_customer_by_phone,
    get_customer_history
)
from billing_functions import (
    create_cart,
    search_products,
    get_product_by_id,
    get_product_by_barcode,
    add_to_cart,
    update_cart_quantity,
    remove_from_cart,
    clear_cart,
    calculate_bill_summary,
    calculate_bill_eco_score,
    complete_bill
)

from receipt_generator import generate_receipt
from customer_functions import find_or_create_customer

# Barcode scanner
from barcode_scanner import scan_barcode


# ============================================================
# GREEN TILL - EMPLOYEE BILLING SCREEN
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


# ============================================================
# COLORS
# ============================================================

GREEN = "#1B5E20"
LIGHT_GREEN = "#E8F5E9"
DARK_GREEN = "#2E7D32"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"
GRAY = "#757575"
RED = "#C62828"
ORANGE = "#EF6C00"


# ============================================================
# BILLING WINDOW
# ============================================================

billing_window = ctk.CTk()

billing_window.title(
    "GreenTill - Employee Billing"
)

billing_window.geometry(
    "1280x760"
)

billing_window.minsize(
    1100,
    650
)


# ============================================================
# CURRENT EMPLOYEE
# ============================================================

CURRENT_EMPLOYEE_ID = "EMP002"

GREEN_TILL_UPI_ID = "greentillstore@upi"
GREEN_TILL_NAME = "GreenTill Supermarket"


# ============================================================
# CART
# ============================================================

cart = create_cart()


# ============================================================
# SELECTED PRODUCT
# ============================================================

selected_product = None


# ============================================================
# FUNCTIONS
# ============================================================


def clear_product_details():

    global selected_product

    selected_product = None

    product_name_label.configure(
        text="No product selected"
    )

    product_category_label.configure(
        text="Category: -"
    )

    product_unit_label.configure(
        text="Unit: -"
    )

    product_price_label.configure(
        text="Price: ₹0.00"
    )

    product_stock_label.configure(
        text="Stock: 0"
    )

    quantity_entry.delete(
        0,
        "end"
    )

    quantity_entry.insert(
        0,
        "1"
    )


# ============================================================
# SHOW PRODUCT
# ============================================================

def show_product(product):

    global selected_product

    selected_product = product

    product_name_label.configure(
        text=product["name"]
    )

    product_category_label.configure(
        text=f"Category: {product['category']}"
    )

    product_unit_label.configure(
        text=f"Unit: {product['unit']}"
    )

    product_price_label.configure(
        text=f"Price: ₹{product['price']:.2f}"
    )

    product_stock_label.configure(
        text=(
            f"Stock: {product['stock']:.2f} "
            f"{product['unit']}"
        )
    )

    quantity_entry.delete(
        0,
        "end"
    )

    quantity_entry.insert(
        0,
        "1"
    )


# ============================================================
# SEARCH PRODUCT
# ============================================================

def search_product():

    search_text = search_entry.get().strip()

    if not search_text:

        messagebox.showwarning(
            "Search Product",
            "Please enter a product name, ID or barcode."
        )

        return

    products = search_products(
        search_text
    )

    if not products:

        messagebox.showinfo(
            "Product Not Found",
            "No active product found."
        )

        return

    # Show first matching product
    show_product(
        products[0]
    )


# ============================================================
# FIND PRODUCT BY ID / BARCODE
# ============================================================

def find_product_by_id_or_barcode():

    search_text = search_entry.get().strip()

    if not search_text:

        messagebox.showwarning(
            "Search Product",
            "Please enter a product ID or barcode."
        )

        return

    # Try Product ID first
    product = get_product_by_id(
        search_text
    )

    # If not found, try barcode
    if product is None:

        product = get_product_by_barcode(
            search_text
        )

    if product is None:

        messagebox.showinfo(
            "Product Not Found",
            "No product found with this ID or barcode."
        )

        return

    if product["status"] != "Active":

        messagebox.showwarning(
            "Inactive Product",
            "This product is currently inactive."
        )

        return

    show_product(
        product
    )


# ============================================================
# SCAN BARCODE
# ============================================================

def scan_product_barcode():

    try:

        # Open camera and scan
        barcode = scan_barcode()

        if not barcode:

            messagebox.showinfo(
                "Barcode Scanner",
                "No barcode was detected."
            )

            return

        barcode = str(
            barcode
        ).strip()

        print(
            f"GreenTill scanned barcode: {barcode}"
        )

        # ----------------------------------------------------
        # Find product using barcode
        # ----------------------------------------------------

        product = get_product_by_barcode(
            barcode
        )

        if product is None:

            messagebox.showwarning(
                "Product Not Found",
                (
                    f"Barcode scanned successfully:\n\n"
                    f"{barcode}\n\n"
                    "But no product is registered "
                    "with this barcode."
                )
            )

            return

        # ----------------------------------------------------
        # Check product status
        # ----------------------------------------------------

        if product["status"] != "Active":

            messagebox.showwarning(
                "Inactive Product",
                (
                    f"{product['name']} is currently "
                    "inactive and cannot be added to the bill."
                )
            )

            return

        # ----------------------------------------------------
        # Display product details
        # ----------------------------------------------------

        show_product(
            product
        )

        # ----------------------------------------------------
        # Automatically add one quantity to cart
        # ----------------------------------------------------

        add_to_cart(
            cart,
            product,
            1
        )

        # ----------------------------------------------------
        # Refresh cart and totals
        # ----------------------------------------------------

        refresh_cart()

        

    except Exception as error:

        messagebox.showerror(
            "Barcode Scanner Error",
            str(error)
        )


# ============================================================
# ADD SELECTED PRODUCT
# ============================================================

def add_selected_product():

    if selected_product is None:

        messagebox.showwarning(
            "Add Product",
            "Please search and select a product first."
        )

        return

    try:

        quantity = float(
            quantity_entry.get()
        )

        if quantity <= 0:

            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a valid quantity."
        )

        return

    try:

        add_to_cart(
            cart,
            selected_product,
            quantity
        )

        refresh_cart()


    except Exception as error:

        messagebox.showerror(
            "Unable to Add Product",
            str(error)
        )


# ============================================================
# REFRESH CART
# ============================================================

def refresh_cart():

    # Remove old cart rows
    for widget in cart_items_frame.winfo_children():

        widget.destroy()

    if not cart:

        empty_cart_label = ctk.CTkLabel(
            cart_items_frame,
            text="Cart is empty",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=GRAY
        )

        empty_cart_label.pack(
            pady=40
        )

    else:

        for item in cart:

            item_frame = ctk.CTkFrame(
                cart_items_frame,
                fg_color=WHITE,
                corner_radius=8
            )

            item_frame.pack(
                fill="x",
                padx=5,
                pady=4
            )

            # ------------------------------------------------
            # Product name
            # ------------------------------------------------

            name_label = ctk.CTkLabel(
                item_frame,
                text=item["name"],
                width=150,
                anchor="w",
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            )

            name_label.grid(
                row=0,
                column=0,
                padx=8,
                pady=8
            )

            # ------------------------------------------------
            # Quantity
            # ------------------------------------------------

            quantity_label = ctk.CTkLabel(
                item_frame,
                text=(
                    f"{item['quantity']:.2f} "
                    f"{item['unit']}"
                ),
                width=100
            )

            quantity_label.grid(
                row=0,
                column=1,
                padx=5
            )

            # ------------------------------------------------
            # Price
            # ------------------------------------------------

            price_label = ctk.CTkLabel(
                item_frame,
                text=f"₹{item['unit_price']:.2f}",
                width=80
            )

            price_label.grid(
                row=0,
                column=2,
                padx=5
            )

            # ------------------------------------------------
            # Item total
            # ------------------------------------------------

            total_label = ctk.CTkLabel(
                item_frame,
                text=f"₹{item['item_total']:.2f}",
                width=90,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            )

            total_label.grid(
                row=0,
                column=3,
                padx=5
            )

            # ------------------------------------------------
            # Remove button
            # ------------------------------------------------

            remove_button = ctk.CTkButton(
                item_frame,
                text="Remove",
                width=75,
                height=30,
                fg_color=RED,
                hover_color="#8E0000",
                command=lambda
                pid=item["product_id"]:
                remove_item(pid)
            )

            remove_button.grid(
                row=0,
                column=4,
                padx=8
            )

    update_summary()


# ============================================================
# REMOVE ITEM
# ============================================================

def remove_item(product_id):

    try:

        remove_from_cart(
            cart,
            product_id
        )

        refresh_cart()

    except Exception as error:

        messagebox.showerror(
            "Remove Product",
            str(error)
        )


# ============================================================
# CLEAR CURRENT CART
# ============================================================

def clear_current_cart():

    if not cart:
        return

    confirm = messagebox.askyesno(
        "Clear Cart",
        "Are you sure you want to clear the cart?"
    )

    if confirm:

        clear_cart(
            cart
        )

        refresh_cart()


# ============================================================
# UPDATE BILL SUMMARY
# ============================================================

def update_summary():

    summary = calculate_bill_summary(
        cart,
        discount=0,
        tax_rate=0
    )

    subtotal = summary["subtotal"]
    discount = summary["discount"]
    tax = summary["tax"]
    total = summary["total_amount"]

    eco_score = calculate_bill_eco_score(
        cart
    )

    subtotal_value.configure(
        text=f"₹{subtotal:.2f}"
    )

    discount_value.configure(
        text=f"₹{discount:.2f}"
    )

    tax_value.configure(
        text=f"₹{tax:.2f}"
    )

    total_value.configure(
        text=f"₹{total:.2f}"
    )

    eco_score_value.configure(
        text=str(eco_score)
    )


# ============================================================
# PAYMENT
# ============================================================
def start_payment():

    if not cart:
        messagebox.showwarning(
            "Payment",
            "Cart is empty. Add products before payment."
        )
        return

    payment_window = ctk.CTkToplevel(billing_window)
    payment_window.title("GreenTill - Payment")
    payment_window.geometry("520x680")
    payment_window.resizable(False, False)
    payment_window.transient(billing_window)
    payment_window.grab_set()

    summary = calculate_bill_summary(
        cart,
        discount=0,
        tax_rate=0
    )

    total_amount = summary["total_amount"]

    ctk.CTkLabel(
        payment_window,
        text="Complete Payment",
        font=ctk.CTkFont(size=24, weight="(
        payment_window,
        text="CUSTOMER HISTORY",
        width=200,
        height=38,
        fg_color=DARK_GREEN,
        hover_color="#17482D",
        command=lambda: open_customer_history(
            payment_window,bold"),
        text_color=GREEN
    ).pack(pady=(25, 8))
    ctk.CTkButton
            customer_phone_entry.get()
        )
    ).pack(pady=(5, 10))

    ctk.CTkLabel(
        payment_window,
        text=f"Amount Payable: ₹{total_amount:.2f}",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=GREEN
    ).pack(pady=(0, 20))

    ctk.CTkLabel(
        payment_window,
        text="Select Payment Method",
        font=ctk.CTkFont(size=15, weight="bold")
    ).pack(pady=(0, 10))

    payment_method = ctk.StringVar(value="Cash")

    payment_options_frame = ctk.CTkFrame(
        payment_window,
        fg_color="transparent"
    )
    payment_options_frame.pack(pady=5)

    upi_frame = ctk.CTkFrame(
        payment_window,
        fg_color=LIGHT_GREEN,
        corner_radius=10
    )
    upi_frame.pack(
        fill="x",
        padx=30,
        pady=15
    )

    upi_status_label = ctk.CTkLabel(
        upi_frame,
        text="Select UPI to display payment QR",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=GREEN
    )
    upi_status_label.pack(pady=(12, 5))

    qr_label = ctk.CTkLabel(
        upi_frame,
        text=""
    )
    qr_label.pack(pady=5)

    upi_id_label = ctk.CTkLabel(
        upi_frame,
        text=""
    )
    upi_id_label.pack(pady=(2, 12))

    qr_label.image = None

    def create_upi_qr():

        try:

            # ----------------------------------------------------
            # Create UPI payment URI
            # ----------------------------------------------------

            upi_uri = (
                "upi://pay?"
                f"pa={quote(GREEN_TILL_UPI_ID)}"
                f"&pn={quote(GREEN_TILL_NAME)}"
                f"&am={total_amount:.2f}"
                "&cu=INR"
            )

            # ----------------------------------------------------
            # Generate QR code
            # ----------------------------------------------------

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4
            )

            qr.add_data(upi_uri)
            qr.make(fit=True)

            qr_image = qr.make_image(
                fill_color="black",
                back_color="white"
            ).convert("RGB")

            qr_image = qr_image.resize(
                (240, 240)
            )

            # IMPORTANT:
            # This application uses more than one CTk() root window.
            # The PhotoImage MUST belong to the same Tk interpreter
            # as qr_label. Otherwise Tk can raise:
            # "image 'pyimage2' doesn't exist".
            qr_photo = ImageTk.PhotoImage(
                qr_image,
                master=qr_label
            )

            qr_label.configure(
                image=qr_photo,
                text=""
            )

            # Keep a reference so Python does not garbage-collect it.
            qr_label.image = qr_photo

            upi_status_label.configure(
                text="Scan this QR using your UPI app"
            )

            upi_id_label.configure(
                text=(
                    f"UPI ID: {GREEN_TILL_UPI_ID}\n"
                    f"Amount: ₹{total_amount:.2f}"
                )
            )

        except Exception as error:

            qr_label.configure(
                image="",
                text="QR could not be generated"
            )

            qr_label.image = None

            upi_status_label.configure(
                text="Unable to generate UPI QR"
            )

            upi_id_label.configure(
                text=f"UPI ID: {GREEN_TILL_UPI_ID}"
            )

            messagebox.showerror(
                "UPI QR Error",
                f"Unable to generate UPI QR code.\n\n{error}",
                parent=payment_window
            )

    def hide_upi_qr():

        qr_label.configure(
            image="",
            text=""
        )

        qr_label.image = None

        upi_status_label.configure(
            text="Select UPI to display payment QR"
        )

        upi_id_label.configure(
            text=""
        )

    def payment_method_changed():

        selected_method = payment_method.get()

        if selected_method == "UPI":
            create_upi_qr()
            confirm_button.configure(
                text="PAYMENT COMPLETED"
            )
        else:
            hide_upi_qr()
            confirm_button.configure(
                text="CONFIRM PAYMENT"
            )

    ctk.CTkRadioButton(
        payment_options_frame,
        text="Cash",
        variable=payment_method,
        value="Cash",
        command=payment_method_changed
    ).pack(side="left", padx=15)

    ctk.CTkRadioButton(
        payment_options_frame,
        text="UPI",
        variable=payment_method,
        value="UPI",
        command=payment_method_changed
    ).pack(side="left", padx=15)

    ctk.CTkRadioButton(
        payment_options_frame,
        text="Card",
        variable=payment_method,
        value="Card",
        command=payment_method_changed
    ).pack(side="left", padx=15)

    def show_bill_and_print_window(bill, receipt_file):

        receipt_window = ctk.CTkToplevel(billing_window)
        receipt_window.title("GreenTill - Bill & Receipt")
        receipt_window.geometry("700x700")
        receipt_window.minsize(620, 600)
        receipt_window.transient(billing_window)
        receipt_window.grab_set()

        ctk.CTkLabel(
            receipt_window,
            text="Bill Completed",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=GREEN
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            receipt_window,
            text=(
                f"Bill No: {bill['bill_id']}    "
                f"Payment: {bill['payment_method']}    "
                f"Total: ₹{bill['total_amount']:.2f}"
            ),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(0, 12))

        receipt_text = ctk.CTkTextbox(
            receipt_window,
            width=620,
            height=500,
            font=("Consolas", 12)
        )
        receipt_text.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        receipt_text.insert(
            "1.0",
            (
                "GREEN TILL\n"
                "Smart Billing. Greener Shopping.\n"
                "----------------------------------------\n"
                f"Bill No : {bill['bill_id']}\n"
                f"Date    : {bill.get('bill_date', '')}\n"
                f"Time    : {bill.get('bill_time', '')}\n"
                f"Payment : {bill['payment_method']}\n"
                "----------------------------------------\n"
            )
        )

        try:
            from billing_functions import get_bill_items

            items = get_bill_items(bill["bill_id"])

            for item in items:
                # sqlite3.Row does not support .get().
                # Read its fields using [] and use the product table
                # to obtain the product name and unit.
                product_id = item["product_id"]
                product = get_product_by_id(product_id)

                if product:
                    product_name = product["name"]
                    unit = product["unit"]
                else:
                    product_name = product_id
                    unit = ""

                quantity = float(item["quantity"])
                unit_price = float(item["unit_price"])
                item_total = float(item["item_total"])

                receipt_text.insert(
                    "end",
                    (
                        f"{product_name}\n"
                        f"  {quantity:.2f} {unit} x "
                        f"₹{unit_price:.2f} = "
                        f"₹{item_total:.2f}\n"
                    )
                )

        except Exception as error:
            receipt_text.insert(
                "end",
                f"\nUnable to load bill items: {error}\n"
            )

        receipt_text.insert(
            "end",
            (
                "----------------------------------------\n"
                f"Subtotal : ₹{bill['subtotal']:.2f}\n"
                f"Discount : ₹{bill['discount']:.2f}\n"
                f"Tax      : ₹{bill['tax']:.2f}\n"
                f"TOTAL    : ₹{bill['total_amount']:.2f}\n"
                "----------------------------------------\n"
                f"Eco Score: {bill['eco_score']}\n\n"
                f"PDF Receipt:\n{receipt_file}\n"
            )
        )

        receipt_text.configure(state="disabled")

        button_frame = ctk.CTkFrame(
            receipt_window,
            fg_color="transparent"
        )
        button_frame.pack(pady=(5, 20))

        def open_pdf():

            try:
                import os
                os.startfile(str(receipt_file))
            except Exception as error:
                messagebox.showerror(
                    "Open Receipt",
                    str(error),
                    parent=receipt_window
                )

        def print_receipt():

            try:
                import os

                # Windows may not have a "print" shell verb registered
                # for the default PDF application. Open the generated PDF
                # instead so the cashier can use the viewer's Print command
                # and select the required Windows printer.
                os.startfile(str(receipt_file))

            except Exception as error:
                messagebox.showerror(
                    "Print Receipt",
                    (
                        "Unable to open the receipt for printing.\n\n"
                        f"{error}"
                    ),
                    parent=receipt_window
                )

        ctk.CTkButton(
            button_frame,
            text="OPEN PDF",
            width=180,
            height=42,
            fg_color="#388E3C",
            hover_color=DARK_GREEN,
            command=open_pdf
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="PRINT RECEIPT",
            width=180,
            height=42,
            fg_color=GREEN,
            hover_color=DARK_GREEN,
            command=print_receipt
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_frame,
            text="CLOSE",
            width=120,
            height=42,
            fg_color=GRAY,
            hover_color="#555555",
            command=receipt_window.destroy
        ).pack(side="left", padx=8)

    def confirm_payment():

        selected_method = payment_method.get()

        if not selected_method:
            messagebox.showwarning(
                "Payment Method",
                "Please select a payment method.",
                parent=payment_window
            )
            return

        try:

            # ------------------------------------------------
            # CUSTOMER DETAILS
            # ------------------------------------------------

            customer_name = customer_name_entry.get().strip()
            customer_phone = customer_phone_entry.get().strip()

            customer_id = find_or_create_customer(
                customer_name,
                customer_phone
            )

            # ------------------------------------------------
            # COMPLETE BILL
            # ------------------------------------------------

            bill = complete_bill(
                CURRENT_EMPLOYEE_ID,
                cart,
                selected_method,
                customer_id=customer_id
            )

            bill_id = bill["bill_id"]

            # ------------------------------------------------
            # GENERATE RECEIPT
            # ------------------------------------------------

            receipt_file = generate_receipt(
                bill_id
            )

            # ------------------------------------------------
            # CLEAR CART
            # ------------------------------------------------

            clear_cart(cart)
            refresh_cart()

            # ------------------------------------------------
            # CLOSE PAYMENT WINDOW
            # ------------------------------------------------

            payment_window.destroy()

            # ------------------------------------------------
            # SHOW BILL
            # ------------------------------------------------

            show_bill_and_print_window(
                bill,
                receipt_file
            )

        except Exception as error:

            messagebox.showerror(
                "Payment Failed",
                str(error),
                parent=payment_window
            )

    confirm_button = ctk.CTkButton(
        payment_window,
        text="CONFIRM PAYMENT",
        width=300,
        height=45,
        font=ctk.CTkFont(
            size=14,
            weight="bold"
        ),
        fg_color=GREEN,
        hover_color=DARK_GREEN,
        command=confirm_payment
    )
    confirm_button.pack(pady=(15, 8))

    ctk.CTkButton(
        payment_window,
        text="CANCEL",
        width=300,
        height=38,
        fg_color=GRAY,
        hover_color="#555555",
        command=payment_window.destroy
    ).pack(pady=5)


# ============================================================
# HEADER
# ============================================================

header = ctk.CTkFrame(
    billing_window,
    height=70,
    fg_color=GREEN,
    corner_radius=0
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)


title_label = ctk.CTkLabel(
    header,
    text="GreenTill",
    font=ctk.CTkFont(
        size=28,
        weight="bold"
    ),
    text_color=WHITE
)

title_label.pack(
    side="left",
    padx=25
)


subtitle_label = ctk.CTkLabel(
    header,
    text="Smart Billing. Greener Shopping.",
    font=ctk.CTkFont(
        size=14
    ),
    text_color="#D7FFD9"
)

subtitle_label.pack(
    side="left"
)


employee_label = ctk.CTkLabel(
    header,
    text="Employee: GreenTill Employee",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    ),
    text_color=WHITE
)

employee_label.pack(
    side="right",
    padx=25
)


# ============================================================
# MAIN AREA
# ============================================================

main_frame = ctk.CTkFrame(
    billing_window,
    fg_color=LIGHT_GRAY,
    corner_radius=0
)

main_frame.pack(
    fill="both",
    expand=True
)


main_frame.grid_columnconfigure(
    0,
    weight=1
)

main_frame.grid_columnconfigure(
    1,
    weight=2
)

main_frame.grid_columnconfigure(
    2,
    weight=1
)

main_frame.grid_rowconfigure(
    0,
    weight=1
)


# ============================================================
# LEFT - PRODUCT SEARCH
# ============================================================

product_frame = ctk.CTkFrame(
    main_frame,
    fg_color=WHITE,
    corner_radius=12
)

product_frame.grid(
    row=0,
    column=0,
    padx=15,
    pady=15,
    sticky="nsew"
)


product_title = ctk.CTkLabel(
    product_frame,
    text="Product Search",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    ),
    text_color=GREEN
)

product_title.pack(
    pady=(20, 15)
)


# ------------------------------------------------------------
# SEARCH ENTRY
# ------------------------------------------------------------

search_entry = ctk.CTkEntry(
    product_frame,
    placeholder_text="Product name / ID / barcode",
    height=40
)

search_entry.pack(
    fill="x",
    padx=20,
    pady=5
)


# ------------------------------------------------------------
# SEARCH BUTTON
# ------------------------------------------------------------

search_button = ctk.CTkButton(
    product_frame,
    text="Search Product",
    height=38,
    fg_color=GREEN,
    hover_color=DARK_GREEN,
    command=search_product
)

search_button.pack(
    fill="x",
    padx=20,
    pady=5
)


# ------------------------------------------------------------
# ID / BARCODE BUTTON
# ------------------------------------------------------------

lookup_button = ctk.CTkButton(
    product_frame,
    text="Find by ID / Barcode",
    height=38,
    fg_color="#388E3C",
    hover_color=DARK_GREEN,
    command=find_product_by_id_or_barcode
)

lookup_button.pack(
    fill="x",
    padx=20,
    pady=5
)


# ------------------------------------------------------------
# SCAN BARCODE BUTTON
# ------------------------------------------------------------

scan_button = ctk.CTkButton(
    product_frame,
    text="📷  SCAN BARCODE",
    height=42,
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    ),
    fg_color="#1565C0",
    hover_color="#0D47A1",
    command=scan_product_barcode
)

scan_button.pack(
    fill="x",
    padx=20,
    pady=(8, 12)
)


# ============================================================
# PRODUCT DETAILS
# ============================================================

details_frame = ctk.CTkFrame(
    product_frame,
    fg_color=LIGHT_GREEN,
    corner_radius=10
)

details_frame.pack(
    fill="x",
    padx=20,
    pady=5
)


product_name_label = ctk.CTkLabel(
    details_frame,
    text="No product selected",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    ),
    text_color=GREEN
)

product_name_label.pack(
    pady=(15, 8)
)


product_category_label = ctk.CTkLabel(
    details_frame,
    text="Category: -"
)

product_category_label.pack(
    pady=3
)


product_unit_label = ctk.CTkLabel(
    details_frame,
    text="Unit: -"
)

product_unit_label.pack(
    pady=3
)


product_price_label = ctk.CTkLabel(
    details_frame,
    text="Price: ₹0.00",
    font=ctk.CTkFont(
        size=16,
        weight="bold"
    )
)

product_price_label.pack(
    pady=3
)


product_stock_label = ctk.CTkLabel(
    details_frame,
    text="Stock: 0"
)

product_stock_label.pack(
    pady=(3, 15)
)


# ============================================================
# QUANTITY
# ============================================================

quantity_label = ctk.CTkLabel(
    product_frame,
    text="Quantity",
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    )
)

quantity_label.pack(
    pady=(5, 3)
)


quantity_entry = ctk.CTkEntry(
    product_frame,
    width=120,
    height=38,
    justify="center"
)

quantity_entry.pack(
    pady=5
)

quantity_entry.insert(
    0,
    "1"
)


# ============================================================
# ADD TO CART
# ============================================================

add_button = ctk.CTkButton(
    product_frame,
    text="ADD TO CART",
    height=42,
    font=ctk.CTkFont(
        size=15,
        weight="bold"
    ),
    fg_color=GREEN,
    hover_color=DARK_GREEN,
    command=add_selected_product
)

add_button.pack(
    fill="x",
    padx=20,
    pady=15
)


# ============================================================
# CENTER - SHOPPING CART
# ============================================================

cart_frame = ctk.CTkFrame(
    main_frame,
    fg_color=WHITE,
    corner_radius=12
)

cart_frame.grid(
    row=0,
    column=1,
    padx=5,
    pady=15,
    sticky="nsew"
)


cart_title = ctk.CTkLabel(
    cart_frame,
    text="Shopping Cart",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    ),
    text_color=GREEN
)

cart_title.pack(
    pady=(20, 10)
)


# ============================================================
# CART HEADER
# ============================================================

cart_header = ctk.CTkFrame(
    cart_frame,
    fg_color=LIGHT_GREEN,
    height=40,
    corner_radius=6
)

cart_header.pack(
    fill="x",
    padx=10,
    pady=5
)

cart_header.pack_propagate(
    False
)


headers = [
    ("Product", 150),
    ("Quantity", 100),
    ("Price", 80),
    ("Total", 90),
    ("", 75)
]


for column, (text, width) in enumerate(headers):

    label = ctk.CTkLabel(
        cart_header,
        text=text,
        width=width,
        font=ctk.CTkFont(
            size=12,
            weight="bold"
        )
    )

    label.grid(
        row=0,
        column=column,
        padx=5
    )


# ============================================================
# CART ITEMS AREA
# ============================================================

cart_items_frame = ctk.CTkScrollableFrame(
    cart_frame,
    fg_color=LIGHT_GRAY
)

cart_items_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


# ============================================================
# CLEAR CART
# ============================================================

clear_cart_button = ctk.CTkButton(
    cart_frame,
    text="CLEAR CART",
    height=38,
    fg_color=RED,
    hover_color="#8E0000",
    command=clear_current_cart
)

clear_cart_button.pack(
    fill="x",
    padx=15,
    pady=15
)


# ============================================================
# RIGHT - BILL SUMMARY
# ============================================================

summary_frame = ctk.CTkFrame(
    main_frame,
    fg_color=WHITE,
    corner_radius=12
)

summary_frame.grid(
    row=0,
    column=2,
    padx=15,
    pady=15,
    sticky="nsew"
)


summary_title = ctk.CTkLabel(
    summary_frame,
    text="Bill Summary",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    ),
    text_color=GREEN
)

summary_title.pack(
    pady=(20, 25)
)


# ============================================================
# SUMMARY ROW FUNCTION
# ============================================================

def create_summary_row(
    parent,
    label_text
):

    row = ctk.CTkFrame(
        parent,
        fg_color="transparent"
    )

    row.pack(
        fill="x",
        padx=20,
        pady=8
    )

    label = ctk.CTkLabel(
        row,
        text=label_text,
        font=ctk.CTkFont(
            size=14
        )
    )

    label.pack(
        side="left"
    )

    value = ctk.CTkLabel(
        row,
        text="₹0.00",
        font=ctk.CTkFont(
            size=14,
            weight="bold"
        )
    )

    value.pack(
        side="right"
    )

    return value


subtotal_value = create_summary_row(
    summary_frame,
    "Subtotal"
)


discount_value = create_summary_row(
    summary_frame,
    "Discount"
)


tax_value = create_summary_row(
    summary_frame,
    "Tax"
)


# ============================================================
# SEPARATOR
# ============================================================

separator = ctk.CTkFrame(
    summary_frame,
    height=2,
    fg_color="#DDDDDD"
)

separator.pack(
    fill="x",
    padx=20,
    pady=10
)


# ============================================================
# TOTAL
# ============================================================

total_row = ctk.CTkFrame(
    summary_frame,
    fg_color=LIGHT_GREEN,
    corner_radius=8
)

total_row.pack(
    fill="x",
    padx=15,
    pady=10
)


total_label = ctk.CTkLabel(
    total_row,
    text="TOTAL",
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    ),
    text_color=GREEN
)

total_label.pack(
    side="left",
    padx=15,
    pady=15
)


total_value = ctk.CTkLabel(
    total_row,
    text="₹0.00",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    ),
    text_color=GREEN
)

total_value.pack(
    side="right",
    padx=15
)


# ============================================================
# ECO SCORE
# ============================================================

eco_frame = ctk.CTkFrame(
    summary_frame,
    fg_color="#E0F2F1",
    corner_radius=8
)

eco_frame.pack(
    fill="x",
    padx=15,
    pady=15
)


eco_title = ctk.CTkLabel(
    eco_frame,
    text="🌱 Eco Score",
    font=ctk.CTkFont(
        size=15,
        weight="bold"
    )
)

eco_title.pack(
    side="left",
    padx=15,
    pady=12
)


eco_score_value = ctk.CTkLabel(
    eco_frame,
    text="0",
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    ),
    text_color=GREEN
)

eco_score_value.pack(
    side="right",
    padx=15
)
# ============================================================
# CUSTOMER DETAILS - OPTIONAL
# ============================================================

customer_details_frame = ctk.CTkFrame(
    summary_frame,
    fg_color=LIGHT_GREEN,
    corner_radius=8
)

customer_details_frame.pack(
    fill="x",
    padx=15,
    pady=(10, 5)
)

customer_details_title = ctk.CTkLabel(
    customer_details_frame,
    text="Customer Details (Optional)",
    font=ctk.CTkFont(
        size=15,
        weight="bold"
    ),
    text_color=GREEN
)

customer_details_title.pack(
    pady=(12, 8)
)

customer_name_entry = ctk.CTkEntry(
    customer_details_frame,
    placeholder_text="Customer Full Name",
    height=36
)

customer_name_entry.pack(
    fill="x",
    padx=15,
    pady=5
)

customer_phone_entry = ctk.CTkEntry(
    customer_details_frame,
    placeholder_text="Phone Number",
    height=36
)

customer_phone_entry.pack(
    fill="x",
    padx=15,
    pady=(5, 12)
)

# ============================================================
# PAYMENT BUTTON
# ============================================================

payment_button = ctk.CTkButton(
    summary_frame,
    text="PROCEED TO PAYMENT",
    height=48,
    font=ctk.CTkFont(
        size=15,
        weight="bold"
    ),
    fg_color=GREEN,
    hover_color=DARK_GREEN,
    command=start_payment
)

payment_button.pack(
    fill="x",
    padx=20,
    pady=(30, 10)
)


# ============================================================
# INITIAL STATE
# ============================================================

clear_product_details()

refresh_cart()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    billing_window.mainloop()