import customtkinter as ctk
from tkinter import messagebox
from database import get_connection
from datetime import datetime, date


# ============================================================
# GreenTill - Admin Dashboard
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


# ============================================================
# Colors
# ============================================================

BG = "#F4FAF3"
WHITE = "#FFFFFF"

DARK_GREEN = "#146B43"
GREEN = "#249B56"
GREEN_HOVER = "#188047"

TEXT = "#18342A"
GRAY = "#708078"

SIDEBAR = "#123F2C"
SIDEBAR_HOVER = "#1D6043"

BORDER = "#D5E8DC"


# ============================================================
# Main Window
# ============================================================

dashboard = ctk.CTk()

dashboard.title("GreenTill - Admin Dashboard")
dashboard.geometry("1280x760")
dashboard.resizable(False, False)
dashboard.configure(fg_color=BG)


# ============================================================
# Employee Management
# ============================================================

def open_employee_management():

    employee_window = ctk.CTkToplevel(dashboard)

    employee_window.title("GreenTill - Employee Management")
    employee_window.geometry("1050x650")
    employee_window.resizable(False, False)
    employee_window.configure(fg_color=BG)

    employee_window.transient(dashboard)

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    header = ctk.CTkFrame(
        employee_window,
        height=90,
        corner_radius=0,
        fg_color=WHITE,
        border_width=1,
        border_color=BORDER
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    header_left = ctk.CTkFrame(
        header,
        fg_color="transparent"
    )

    header_left.pack(
        side="left",
        padx=30
    )

    ctk.CTkLabel(
        header_left,
        text="👥  Employee Management",
        font=ctk.CTkFont(
            family="Arial",
            size=24,
            weight="bold"
        ),
        text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
        header_left,
        text="Manage GreenTill employees and cashier accounts",
        font=ctk.CTkFont(
            family="Arial",
            size=12
        ),
        text_color=GRAY
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    # --------------------------------------------------------
    # Add Employee Button
    # --------------------------------------------------------

    ctk.CTkButton(
        header,
        text="＋  Add Employee",
        width=150,
        height=42,
        corner_radius=10,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color=WHITE,
        font=ctk.CTkFont(
            family="Arial",
            size=13,
            weight="bold"
        ),
        command=lambda: add_employee(
            employee_window,
            load_employees
        )
    ).pack(
        side="right",
        padx=30
    )

    # --------------------------------------------------------
    # Employee List
    # --------------------------------------------------------

    list_frame = ctk.CTkFrame(
        employee_window,
        fg_color="transparent"
    )

    list_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )

    column_header = ctk.CTkFrame(
        list_frame,
        height=50,
        corner_radius=10,
        fg_color=SIDEBAR
    )

    column_header.pack(fill="x")
    column_header.pack_propagate(False)

    columns = [
        ("Employee ID", 120),
        ("Name", 210),
        ("Username", 160),
        ("Role", 120),
        ("Status", 120),
        ("Action", 130)
    ]

    for title, width in columns:

        ctk.CTkLabel(
            column_header,
            text=title,
            width=width,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold"
            ),
            text_color=WHITE
        ).pack(
            side="left",
            padx=3
        )

    employee_list = ctk.CTkScrollableFrame(
        list_frame,
        fg_color=WHITE,
        corner_radius=12
    )

    employee_list.pack(
        fill="both",
        expand=True,
        pady=(8, 0)
    )

    # --------------------------------------------------------
    # Load Employees
    # --------------------------------------------------------

    def load_employees():

        for widget in employee_list.winfo_children():
            widget.destroy()

        connection = None

        try:

            connection = get_connection()

            employees = connection.execute(
                """
                SELECT employee_id,
                       name,
                       username,
                       role,
                       status
                FROM employees
                ORDER BY employee_id
                """
            ).fetchall()

            if not employees:

                ctk.CTkLabel(
                    employee_list,
                    text="No employees found.",
                    font=ctk.CTkFont(
                        family="Arial",
                        size=15
                    ),
                    text_color=GRAY
                ).pack(pady=50)

                return

            for employee in employees:

                row = ctk.CTkFrame(
                    employee_list,
                    height=58,
                    corner_radius=8,
                    fg_color="#F8FCF9",
                    border_width=1,
                    border_color=BORDER
                )

                row.pack(
                    fill="x",
                    pady=4
                )

                row.pack_propagate(False)

                ctk.CTkLabel(
                    row,
                    text=employee["employee_id"],
                    width=120,
                    text_color=TEXT
                ).pack(side="left", padx=3)

                ctk.CTkLabel(
                    row,
                    text=employee["name"],
                    width=210,
                    anchor="w",
                    text_color=TEXT
                ).pack(side="left", padx=3)

                ctk.CTkLabel(
                    row,
                    text=employee["username"],
                    width=160,
                    anchor="w",
                    text_color=GRAY
                ).pack(side="left", padx=3)

                ctk.CTkLabel(
                    row,
                    text=employee["role"],
                    width=120,
                    text_color=DARK_GREEN
                ).pack(side="left", padx=3)

                status_color = (
                    GREEN
                    if employee["status"] == "Active"
                    else "#A83D3D"
                )

                ctk.CTkLabel(
                    row,
                    text=employee["status"],
                    width=120,
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    ),
                    text_color=status_color
                ).pack(side="left", padx=3)

                new_status = (
                    "Inactive"
                    if employee["status"] == "Active"
                    else "Active"
                )

                ctk.CTkButton(
                    row,
                    text=(
                        "Deactivate"
                        if employee["status"] == "Active"
                        else "Activate"
                    ),
                    width=120,
                    height=32,
                    corner_radius=8,
                    fg_color=(
                        "#F3E7E7"
                        if employee["status"] == "Active"
                        else "#E8F5EC"
                    ),
                    hover_color=(
                        "#EAD5D5"
                        if employee["status"] == "Active"
                        else "#D7EBDD"
                    ),
                    text_color=(
                        "#A83D3D"
                        if employee["status"] == "Active"
                        else GREEN
                    ),
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    ),
                    command=lambda
                    employee_id=employee["employee_id"],
                    status=new_status:
                    change_employee_status(
                        employee_id,
                        status,
                        load_employees
                    )
                ).pack(
                    side="left",
                    padx=5
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load employees.\n\n{error}",
                parent=employee_window
            )

        finally:

            if connection:
                connection.close()

    load_employees()


# ============================================================
# Change Employee Status
# ============================================================

def change_employee_status(
    employee_id,
    new_status,
    refresh_function
):

    connection = None

    try:

        connection = get_connection()

        connection.execute(
            """
            UPDATE employees
            SET status = ?
            WHERE employee_id = ?
            """,
            (new_status, employee_id)
        )

        connection.commit()

        refresh_function()

    except Exception as error:

        messagebox.showerror(
            "Database Error",
            f"Unable to update employee status.\n\n{error}"
        )

    finally:

        if connection:
            connection.close()


# ============================================================
# Add Employee
# ============================================================

def add_employee(parent_window, refresh_function=None):

    add_window = ctk.CTkToplevel(parent_window)

    add_window.title("Add Employee")
    add_window.geometry("500x600")
    add_window.resizable(False, False)
    add_window.configure(fg_color=BG)

    add_window.transient(parent_window)
    add_window.grab_set()

    ctk.CTkLabel(
        add_window,
        text="Add New Employee",
        font=ctk.CTkFont(
            family="Arial",
            size=25,
            weight="bold"
        ),
        text_color=TEXT
    ).pack(pady=(30, 5))

    ctk.CTkLabel(
        add_window,
        text="Create a new GreenTill employee account",
        font=ctk.CTkFont(size=12),
        text_color=GRAY
    ).pack(pady=(0, 25))

    def create_field(label_text, placeholder):

        ctk.CTkLabel(
            add_window,
            text=label_text,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=TEXT,
            anchor="w"
        ).pack(
            fill="x",
            padx=50
        )

        entry = ctk.CTkEntry(
            add_window,
            width=400,
            height=42,
            corner_radius=10,
            fg_color=WHITE,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text=placeholder
        )

        entry.pack(
            padx=50,
            pady=(6, 15)
        )

        return entry

    name_entry = create_field(
        "Full Name",
        "Enter employee name"
    )

    username_entry = create_field(
        "Username",
        "Enter username"
    )

    password_entry = create_field(
        "Password",
        "Enter password"
    )

    ctk.CTkLabel(
        add_window,
        text="Role",
        font=ctk.CTkFont(
            size=13,
            weight="bold"
        ),
        text_color=TEXT,
        anchor="w"
    ).pack(
        fill="x",
        padx=50
    )

    role_dropdown = ctk.CTkOptionMenu(
        add_window,
        width=400,
        height=42,
        corner_radius=10,
        fg_color=GREEN,
        button_color=GREEN,
        button_hover_color=GREEN_HOVER,
        values=[
            "Employee",
            "Admin"
        ]
    )

    role_dropdown.pack(
        padx=50,
        pady=(6, 25)
    )

    def save_employee():

        name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_dropdown.get()

        if not name or not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields.",
                parent=add_window
            )

            return

        connection = None

        try:

            connection = get_connection()

            last_employee = connection.execute(
                """
                SELECT employee_id
                FROM employees
                WHERE employee_id LIKE 'EMP%'
                ORDER BY employee_id DESC
                LIMIT 1
                """
            ).fetchone()

            if last_employee:

                try:
                    last_number = int(
                        last_employee["employee_id"][3:]
                    )
                    new_number = last_number + 1

                except ValueError:
                    new_number = 1

            else:
                new_number = 1

            employee_id = f"EMP{new_number:03d}"

            connection.execute(
                """
                INSERT INTO employees
                (
                    employee_id,
                    name,
                    username,
                    password,
                    role,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_id,
                    name,
                    username,
                    password,
                    role,
                    "Active"
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Employee Added",
                f"Employee created successfully!\n\n"
                f"Employee ID: {employee_id}\n"
                f"Username: {username}\n"
                f"Role: {role}",
                parent=add_window
            )

            add_window.destroy()

            if refresh_function:
                refresh_function()

        except Exception as error:

            if "UNIQUE constraint failed: employees.username" in str(error):

                messagebox.showerror(
                    "Username Already Exists",
                    "This username is already registered.",
                    parent=add_window
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Unable to add employee.\n\n{error}",
                    parent=add_window
                )

        finally:

            if connection:
                connection.close()

    ctk.CTkButton(
        add_window,
        text="＋  CREATE EMPLOYEE",
        width=400,
        height=48,
        corner_radius=11,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color=WHITE,
        font=ctk.CTkFont(
            size=14,
            weight="bold"
        ),
        command=save_employee
    ).pack(padx=50)

    ctk.CTkButton(
        add_window,
        text="Cancel",
        width=400,
        height=40,
        corner_radius=10,
        fg_color="transparent",
        hover_color="#EAF6EC",
        text_color=GRAY,
        command=add_window.destroy
    ).pack(
        padx=50,
        pady=10
    )


# ============================================================
# Product Management
# ============================================================

def open_product_management():

    product_window = ctk.CTkToplevel(dashboard)

    product_window.title("GreenTill - Product Management")
    product_window.geometry("1180x700")
    product_window.resizable(False, False)
    product_window.configure(fg_color=BG)

    product_window.transient(dashboard)

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    header = ctk.CTkFrame(
        product_window,
        height=90,
        corner_radius=0,
        fg_color=WHITE,
        border_width=1,
        border_color=BORDER
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    header_left = ctk.CTkFrame(
        header,
        fg_color="transparent"
    )

    header_left.pack(
        side="left",
        padx=30
    )

    ctk.CTkLabel(
        header_left,
        text="📦  Product Management",
        font=ctk.CTkFont(
            family="Arial",
            size=24,
            weight="bold"
        ),
        text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
        header_left,
        text="Manage fruits, vegetables, groceries and all supermarket products",
        font=ctk.CTkFont(size=12),
        text_color=GRAY
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    ctk.CTkButton(
        header,
        text="＋  Add Product",
        width=150,
        height=42,
        corner_radius=10,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color=WHITE,
        font=ctk.CTkFont(
            size=13,
            weight="bold"
        ),
        command=lambda: add_product(product_window)
    ).pack(
        side="right",
        padx=30
    )

    # --------------------------------------------------------
    # Search / Filters
    # --------------------------------------------------------

    filter_frame = ctk.CTkFrame(
        product_window,
        height=75,
        fg_color="transparent"
    )

    filter_frame.pack(
        fill="x",
        padx=30,
        pady=(20, 5)
    )

    filter_frame.pack_propagate(False)

    search_entry = ctk.CTkEntry(
        filter_frame,
        width=350,
        height=42,
        corner_radius=10,
        fg_color=WHITE,
        border_color=BORDER,
        text_color=TEXT,
        placeholder_text="🔍  Search product or barcode..."
    )

    search_entry.pack(side="left")

    category_menu = ctk.CTkOptionMenu(
        filter_frame,
        width=190,
        height=42,
        corner_radius=10,
        fg_color=WHITE,
        button_color=GREEN,
        button_hover_color=GREEN_HOVER,
        text_color=TEXT,
        values=[
            "All Categories",
            "Vegetables",
            "Fruits",
            "Dairy",
            "Grocery",
            "Snacks",
            "Beverages",
            "Personal Care",
            "Household"
        ]
    )

    category_menu.pack(
        side="left",
        padx=12
    )

    status_menu = ctk.CTkOptionMenu(
        filter_frame,
        width=150,
        height=42,
        corner_radius=10,
        fg_color=WHITE,
        button_color=GREEN,
        button_hover_color=GREEN_HOVER,
        text_color=TEXT,
        values=[
            "All Status",
            "Active",
            "Inactive"
        ]
    )

    status_menu.pack(side="left")

    # --------------------------------------------------------
    # Product List
    # --------------------------------------------------------

    list_frame = ctk.CTkFrame(
        product_window,
        fg_color="transparent"
    )

    list_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(10, 25)
    )

    column_header = ctk.CTkFrame(
        list_frame,
        height=48,
        corner_radius=10,
        fg_color=SIDEBAR
    )

    column_header.pack(fill="x")
    column_header.pack_propagate(False)

    columns = [
        ("ID", 70),
        ("Product", 180),
        ("Category", 125),
        ("Unit", 75),
        ("Price", 90),
        ("Stock", 85),
        ("Eco", 65),
        ("Expiry", 100),
        ("Status", 90),
        ("Action", 130)
    ]

    for title, width in columns:

        ctk.CTkLabel(
            column_header,
            text=title,
            width=width,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=WHITE
        ).pack(
            side="left",
            padx=2
        )

    product_list = ctk.CTkScrollableFrame(
        list_frame,
        fg_color=WHITE,
        corner_radius=12
    )

    product_list.pack(
        fill="both",
        expand=True,
        pady=(7, 0)
    )

    # --------------------------------------------------------
    # Load Products
    # --------------------------------------------------------

    def load_products():

        for widget in product_list.winfo_children():
            widget.destroy()

        search_text = search_entry.get().strip().lower()
        selected_category = category_menu.get()
        selected_status = status_menu.get()

        connection = None

        try:

            connection = get_connection()

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
                ORDER BY product_id
                """
            ).fetchall()

            filtered_products = []

            for product in products:

                if search_text:

                    product_name = product["name"].lower()

                    barcode = (
                        str(product["barcode"]).lower()
                        if product["barcode"]
                        else ""
                    )

                    product_id = product["product_id"].lower()

                    if (
                        search_text not in product_name
                        and search_text not in barcode
                        and search_text not in product_id
                    ):
                        continue

                if (
                    selected_category != "All Categories"
                    and product["category"] != selected_category
                ):
                    continue

                if (
                    selected_status != "All Status"
                    and product["status"] != selected_status
                ):
                    continue

                filtered_products.append(product)

            if not filtered_products:

                ctk.CTkLabel(
                    product_list,
                    text="No products found.",
                    font=ctk.CTkFont(size=15),
                    text_color=GRAY
                ).pack(pady=60)

                return

            for product in filtered_products:

                row = ctk.CTkFrame(
                    product_list,
                    height=58,
                    corner_radius=8,
                    fg_color="#F8FCF9",
                    border_width=1,
                    border_color=BORDER
                )

                row.pack(
                    fill="x",
                    pady=3
                )

                row.pack_propagate(False)

                ctk.CTkLabel(
                    row,
                    text=product["product_id"],
                    width=70,
                    text_color=TEXT
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=product["name"],
                    width=180,
                    anchor="w",
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    ),
                    text_color=TEXT
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=product["category"],
                    width=125,
                    anchor="w",
                    text_color=GRAY
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=product["unit"],
                    width=75,
                    text_color=TEXT
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=f"₹{product['price']:.2f}",
                    width=90,
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    ),
                    text_color=DARK_GREEN
                ).pack(side="left", padx=2)

                stock = float(product["stock"])
                reorder = float(product["reorder_level"])

                stock_color = (
                    "#C0392B"
                    if stock <= reorder
                    else GREEN
                )

                ctk.CTkLabel(
                    row,
                    text=f"{stock:g} {product['unit']}",
                    width=85,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    ),
                    text_color=stock_color
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=f"{product['eco_score']}/100",
                    width=65,
                    text_color=DARK_GREEN
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=product["expiry_date"] or "N/A",
                    width=100,
                    text_color=GRAY
                ).pack(side="left", padx=2)

                status_color = (
                    GREEN
                    if product["status"] == "Active"
                    else "#A83D3D"
                )

                ctk.CTkLabel(
                    row,
                    text=product["status"],
                    width=90,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    ),
                    text_color=status_color
                ).pack(side="left", padx=2)

                action_frame = ctk.CTkFrame(
                    row,
                    width=130,
                    fg_color="transparent"
                )

                action_frame.pack(
                    side="left",
                    padx=2
                )

                ctk.CTkButton(
                    action_frame,
                    text="Edit",
                    width=55,
                    height=30,
                    corner_radius=7,
                    fg_color="#EAF6EC",
                    hover_color="#D8EEDF",
                    text_color=DARK_GREEN,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    ),
                    command=lambda p=dict(product):
                    edit_product(
                        product_window,
                        p,
                        load_products
                    )
                ).pack(side="left", padx=2)

                new_status = (
                    "Inactive"
                    if product["status"] == "Active"
                    else "Active"
                )

                ctk.CTkButton(
                    action_frame,
                    text=(
                        "Off"
                        if product["status"] == "Active"
                        else "On"
                    ),
                    width=45,
                    height=30,
                    corner_radius=7,
                    fg_color=(
                        "#F3E7E7"
                        if product["status"] == "Active"
                        else "#EAF6EC"
                    ),
                    hover_color=(
                        "#EAD5D5"
                        if product["status"] == "Active"
                        else "#D8EEDF"
                    ),
                    text_color=(
                        "#A83D3D"
                        if product["status"] == "Active"
                        else GREEN
                    ),
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    ),
                    command=lambda
                    pid=product["product_id"],
                    status=new_status:
                    change_product_status(
                        pid,
                        status,
                        load_products
                    )
                ).pack(side="left", padx=2)

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load products.\n\n{error}",
                parent=product_window
            )

        finally:

            if connection:
                connection.close()

    search_entry.bind(
        "<KeyRelease>",
        lambda event: load_products()
    )

    category_menu.configure(
        command=lambda choice: load_products()
    )

    status_menu.configure(
        command=lambda choice: load_products()
    )

    load_products()


# ============================================================
# Change Product Status
# ============================================================

def change_product_status(
    product_id,
    new_status,
    refresh_function
):

    connection = None

    try:

        connection = get_connection()

        connection.execute(
            """
            UPDATE products
            SET status = ?
            WHERE product_id = ?
            """,
            (new_status, product_id)
        )

        connection.commit()

        refresh_function()

    except Exception as error:

        messagebox.showerror(
            "Database Error",
            f"Unable to update product status.\n\n{error}"
        )

    finally:

        if connection:
            connection.close()


# ============================================================
# Add Product
# ============================================================

def add_product(parent_window):

    add_window = ctk.CTkToplevel(parent_window)

    add_window.title("Add Product")
    add_window.geometry("550x720")
    add_window.resizable(False, False)
    add_window.configure(fg_color=BG)

    add_window.transient(parent_window)
    add_window.grab_set()

    ctk.CTkLabel(
        add_window,
        text="Add New Product",
        font=ctk.CTkFont(
            size=25,
            weight="bold"
        ),
        text_color=TEXT
    ).pack(pady=(25, 4))

    ctk.CTkLabel(
        add_window,
        text="Add a supermarket product to GreenTill",
        font=ctk.CTkFont(size=12),
        text_color=GRAY
    ).pack(pady=(0, 20))

    def create_field(label, placeholder):

        ctk.CTkLabel(
            add_window,
            text=label,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT,
            anchor="w"
        ).pack(
            fill="x",
            padx=45
        )

        entry = ctk.CTkEntry(
            add_window,
            width=460,
            height=38,
            corner_radius=9,
            fg_color=WHITE,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text=placeholder
        )

        entry.pack(
            padx=45,
            pady=(5, 10)
        )

        return entry

    product_id_entry = create_field(
        "Product ID",
        "Example: P015"
    )

    barcode_entry = create_field(
        "Barcode",
        "Optional - for barcode scanner"
    )

    name_entry = create_field(
        "Product Name",
        "Example: Mango"
    )

    ctk.CTkLabel(
        add_window,
        text="Category",
        font=ctk.CTkFont(
            size=12,
            weight="bold"
        ),
        text_color=TEXT,
        anchor="w"
    ).pack(
        fill="x",
        padx=45
    )

    category_menu = ctk.CTkOptionMenu(
        add_window,
        width=460,
        height=38,
        corner_radius=9,
        fg_color=GREEN,
        button_color=GREEN,
        button_hover_color=GREEN_HOVER,
        values=[
            "Vegetables",
            "Fruits",
            "Dairy",
            "Grocery",
            "Snacks",
            "Beverages",
            "Personal Care",
            "Household"
        ]
    )

    category_menu.pack(
        padx=45,
        pady=(5, 10)
    )

    ctk.CTkLabel(
        add_window,
        text="Unit",
        font=ctk.CTkFont(
            size=12,
            weight="bold"
        ),
        text_color=TEXT,
        anchor="w"
    ).pack(
        fill="x",
        padx=45
    )

    unit_menu = ctk.CTkOptionMenu(
        add_window,
        width=460,
        height=38,
        corner_radius=9,
        fg_color=GREEN,
        button_color=GREEN,
        button_hover_color=GREEN_HOVER,
        values=[
            "Kg",
            "Gram",
            "Piece",
            "Dozen",
            "Liter",
            "ml",
            "Pack",
            "Bottle",
            "Box"
        ]
    )

    unit_menu.pack(
        padx=45,
        pady=(5, 10)
    )

    price_entry = create_field(
        "Price",
        "Price per selected unit"
    )

    stock_entry = create_field(
        "Initial Stock",
        "Example: 25.5"
    )

    reorder_entry = create_field(
        "Reorder Level",
        "Example: 5"
    )

    eco_entry = create_field(
        "Eco Score",
        "0 - 100"
    )

    packaging_entry = create_field(
        "Packaging Type",
        "Loose / Paper / Plastic / etc."
    )

    expiry_entry = create_field(
        "Expiry Date",
        "YYYY-MM-DD or leave blank"
    )

    def save_product():

        product_id = product_id_entry.get().strip()
        barcode = barcode_entry.get().strip()
        name = name_entry.get().strip()
        category = category_menu.get()
        unit = unit_menu.get()
        price = price_entry.get().strip()
        stock = stock_entry.get().strip()
        reorder = reorder_entry.get().strip()
        eco = eco_entry.get().strip()
        packaging = packaging_entry.get().strip()
        expiry = expiry_entry.get().strip()

        if (
            not product_id
            or not name
            or not price
            or not stock
            or not reorder
            or not eco
        ):

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all required fields.",
                parent=add_window
            )

            return

        try:

            price_value = float(price)
            stock_value = float(stock)
            reorder_value = float(reorder)
            eco_value = int(eco)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Price, stock, reorder level and Eco Score\n"
                "must contain valid numbers.",
                parent=add_window
            )

            return

        if (
            price_value < 0
            or stock_value < 0
            or reorder_value < 0
        ):

            messagebox.showerror(
                "Invalid Values",
                "Price, stock and reorder level cannot be negative.",
                parent=add_window
            )

            return

        if eco_value < 0 or eco_value > 100:

            messagebox.showerror(
                "Invalid Eco Score",
                "Eco Score must be between 0 and 100.",
                parent=add_window
            )

            return

        connection = None

        try:

            connection = get_connection()

            connection.execute(
                """
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
                """,
                (
                    product_id,
                    barcode if barcode else None,
                    name,
                    category,
                    unit,
                    price_value,
                    stock_value,
                    reorder_value,
                    eco_value,
                    packaging if packaging else "Not Specified",
                    expiry if expiry else None,
                    "Active"
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Product Added",
                f"Product added successfully!\n\n"
                f"Product ID: {product_id}\n"
                f"Product: {name}",
                parent=add_window
            )

            add_window.destroy()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to add product.\n\n{error}",
                parent=add_window
            )

        finally:

            if connection:
                connection.close()

    ctk.CTkButton(
        add_window,
        text="＋  CREATE PRODUCT",
        width=460,
        height=45,
        corner_radius=10,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color=WHITE,
        font=ctk.CTkFont(
            size=13,
            weight="bold"
        ),
        command=save_product
    ).pack(
        padx=45,
        pady=(5, 8)
    )

    ctk.CTkButton(
        add_window,
        text="Cancel",
        width=460,
        height=38,
        corner_radius=9,
        fg_color="transparent",
        hover_color="#EAF6EC",
        text_color=GRAY,
        command=add_window.destroy
    ).pack(padx=45)


# ============================================================
# Edit Product
# ============================================================

def edit_product(
    parent_window,
    product,
    refresh_function
):

    edit_window = ctk.CTkToplevel(parent_window)

    edit_window.title("Edit Product")
    edit_window.geometry("550x650")
    edit_window.resizable(False, False)
    edit_window.configure(fg_color=BG)

    edit_window.transient(parent_window)
    edit_window.grab_set()

    ctk.CTkLabel(
        edit_window,
        text="Edit Product",
        font=ctk.CTkFont(
            size=25,
            weight="bold"
        ),
        text_color=TEXT
    ).pack(pady=(25, 20))

    def field(label, value):

        ctk.CTkLabel(
            edit_window,
            text=label,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=TEXT,
            anchor="w"
        ).pack(
            fill="x",
            padx=45
        )

        entry = ctk.CTkEntry(
            edit_window,
            width=460,
            height=38,
            corner_radius=9,
            fg_color=WHITE,
            border_color=BORDER,
            text_color=TEXT
        )

        entry.insert(
            0,
            "" if value is None else str(value)
        )

        entry.pack(
            padx=45,
            pady=(5, 10)
        )

        return entry

    name_entry = field("Product Name", product["name"])
    price_entry = field("Price", product["price"])
    stock_entry = field("Stock", product["stock"])
    reorder_entry = field("Reorder Level", product["reorder_level"])
    eco_entry = field("Eco Score", product["eco_score"])
    packaging_entry = field(
        "Packaging Type",
        product["packaging_type"]
    )
    expiry_entry = field(
        "Expiry Date",
        product["expiry_date"]
    )

    def update_product():

        name = name_entry.get().strip()
        price = price_entry.get().strip()
        stock = stock_entry.get().strip()
        reorder = reorder_entry.get().strip()
        eco = eco_entry.get().strip()
        packaging = packaging_entry.get().strip()
        expiry = expiry_entry.get().strip()

        if not name or not price or not stock or not reorder or not eco:

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all required fields.",
                parent=edit_window
            )

            return

        try:

            price_value = float(price)
            stock_value = float(stock)
            reorder_value = float(reorder)
            eco_value = int(eco)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numeric values.",
                parent=edit_window
            )

            return

        if (
            price_value < 0
            or stock_value < 0
            or reorder_value < 0
        ):

            messagebox.showerror(
                "Invalid Values",
                "Price, stock and reorder level cannot be negative.",
                parent=edit_window
            )

            return

        if eco_value < 0 or eco_value > 100:

            messagebox.showerror(
                "Invalid Eco Score",
                "Eco Score must be between 0 and 100.",
                parent=edit_window
            )

            return

        connection = None

        try:

            connection = get_connection()

            connection.execute(
                """
                UPDATE products
                SET
                    name = ?,
                    price = ?,
                    stock = ?,
                    reorder_level = ?,
                    eco_score = ?,
                    packaging_type = ?,
                    expiry_date = ?
                WHERE product_id = ?
                """,
                (
                    name,
                    price_value,
                    stock_value,
                    reorder_value,
                    eco_value,
                    packaging if packaging else "Not Specified",
                    expiry if expiry else None,
                    product["product_id"]
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Product Updated",
                "Product details updated successfully.",
                parent=edit_window
            )

            edit_window.destroy()
            refresh_function()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to update product.\n\n{error}",
                parent=edit_window
            )

        finally:

            if connection:
                connection.close()

    ctk.CTkButton(
        edit_window,
        text="✓  SAVE CHANGES",
        width=460,
        height=45,
        corner_radius=10,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color=WHITE,
        font=ctk.CTkFont(
            size=13,
            weight="bold"
        ),
        command=update_product
    ).pack(
        padx=45,
        pady=(10, 8)
    )

    ctk.CTkButton(
        edit_window,
        text="Cancel",
        width=460,
        height=38,
        corner_radius=9,
        fg_color="transparent",
        hover_color="#EAF6EC",
        text_color=GRAY,
        command=edit_window.destroy
    ).pack(padx=45)


# ============================================================
# INVENTORY MANAGEMENT
# Phase 5.2
# ============================================================

def get_stock_status(stock, reorder_level):

    if stock <= 0:
        return "Out of Stock"

    if stock <= reorder_level:
        return "Low Stock"

    return "In Stock"


def get_expiry_status(expiry_date):

    if not expiry_date:
        return "N/A", GRAY

    try:

        expiry = datetime.strptime(
            expiry_date,
            "%Y-%m-%d"
        ).date()

        today = date.today()

        days_left = (expiry - today).days

        if days_left < 0:
            return "Expired", "#B3261E"

        if days_left <= 7:
            return "Soon", "#B26A00"

        return expiry_date, GRAY

    except ValueError:

        return expiry_date, GRAY


# ============================================================
# Add Stock
# ============================================================

def open_add_stock(
    parent_window,
    selected_product_id=None,
    refresh_function=None
):

    window = ctk.CTkToplevel(parent_window)

    window.title("GreenTill - Add Stock")
    window.geometry("500x500")
    window.resizable(False, False)
    window.configure(fg_color=BG)

    window.transient(parent_window)
    window.grab_set()

    ctk.CTkLabel(
        window,
        text="➕ Add Stock",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        ),
        text_color=DARK_GREEN
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        window,
        text="Add new stock to an existing product",
        font=ctk.CTkFont(size=13),
        text_color=GRAY
    ).pack(pady=(0, 20))

    connection = get_connection()

    products = connection.execute(
        """
        SELECT product_id, name, unit, stock
        FROM products
        WHERE status = 'Active'
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    product_values = [
        f"{p['product_id']} - {p['name']} ({p['unit']})"
        for p in products
    ]

    if not product_values:

        ctk.CTkLabel(
            window,
            text="No active products available.",
            text_color="#B3261E"
        ).pack(pady=20)

        return

    product_menu = ctk.CTkOptionMenu(
        window,
        values=product_values,
        width=380,
        height=40
    )

    product_menu.pack(pady=10)

    if selected_product_id:

        for value in product_values:

            if value.startswith(
                selected_product_id + " -"
            ):

                product_menu.set(value)
                break

    quantity_entry = ctk.CTkEntry(
        window,
        placeholder_text="Quantity to add",
        width=380,
        height=40
    )

    quantity_entry.pack(pady=10)

    reason_entry = ctk.CTkEntry(
        window,
        placeholder_text="Reason (e.g. New supplier delivery)",
        width=380,
        height=40
    )

    reason_entry.pack(pady=10)

    def save_stock():

        selected = product_menu.get()

        if not selected:

            messagebox.showwarning(
                "Select Product",
                "Please select a product.",
                parent=window
            )

            return

        try:

            quantity = float(
                quantity_entry.get().strip()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Please enter a valid quantity greater than 0.",
                parent=window
            )

            return

        product_id = selected.split(" - ")[0]

        reason = reason_entry.get().strip()

        if not reason:
            reason = "Stock received"

        connection = get_connection()

        try:

            product = connection.execute(
                """
                SELECT stock
                FROM products
                WHERE product_id = ?
                """,
                (product_id,)
            ).fetchone()

            if not product:
                raise Exception("Product not found.")

            stock_before = float(
                product["stock"]
            )

            stock_after = (
                stock_before + quantity
            )

            connection.execute(
                """
                UPDATE products
                SET stock = ?
                WHERE product_id = ?
                """,
                (
                    stock_after,
                    product_id
                )
            )

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
                    product_id,
                    "STOCK_IN",
                    quantity,
                    stock_before,
                    stock_after,
                    reason,
                    "EMP001"
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Stock Updated",
                f"Stock added successfully!\n\n"
                f"Previous Stock: {stock_before:g}\n"
                f"Added: {quantity:g}\n"
                f"New Stock: {stock_after:g}",
                parent=window
            )

            window.destroy()

            if refresh_function:
                refresh_function()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                f"Could not update stock.\n\n{error}",
                parent=window
            )

        finally:

            connection.close()

    ctk.CTkButton(
        window,
        text="Save Stock",
        width=380,
        height=42,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        command=save_stock
    ).pack(pady=(20, 10))

    ctk.CTkButton(
        window,
        text="Cancel",
        width=380,
        height=40,
        fg_color="#D9E8DE",
        hover_color="#C5D9CC",
        text_color=DARK_GREEN,
        command=window.destroy
    ).pack()


# ============================================================
# Adjust Stock
# ============================================================

def open_adjust_stock(
    parent_window,
    selected_product_id=None,
    refresh_function=None
):

    window = ctk.CTkToplevel(parent_window)

    window.title("GreenTill - Adjust Stock")
    window.geometry("500x520")
    window.resizable(False, False)
    window.configure(fg_color=BG)

    window.transient(parent_window)
    window.grab_set()

    ctk.CTkLabel(
        window,
        text="🔧 Adjust Stock",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        ),
        text_color=DARK_GREEN
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        window,
        text="Set the correct physical stock quantity",
        font=ctk.CTkFont(
            size=13
        ),
        text_color=GRAY
    ).pack(pady=(0, 20))

    connection = get_connection()

    products = connection.execute(
        """
        SELECT product_id, name, unit, stock
        FROM products
        WHERE status = 'Active'
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    product_values = [
        f"{p['product_id']} - {p['name']} ({p['unit']})"
        for p in products
    ]

    if not product_values:

        ctk.CTkLabel(
            window,
            text="No active products available.",
            text_color="#B3261E"
        ).pack(pady=20)

        return

    product_menu = ctk.CTkOptionMenu(
        window,
        values=product_values,
        width=380,
        height=40
    )

    product_menu.pack(pady=10)

    if selected_product_id:

        for value in product_values:

            if value.startswith(
                selected_product_id + " -"
            ):

                product_menu.set(value)
                break

    new_stock_entry = ctk.CTkEntry(
        window,
        placeholder_text="New physical stock quantity",
        width=380,
        height=40
    )

    new_stock_entry.pack(pady=10)

    reason_entry = ctk.CTkEntry(
        window,
        placeholder_text="Reason (e.g. Damaged / Stock count)",
        width=380,
        height=40
    )

    reason_entry.pack(pady=10)

    def save_adjustment():

        selected = product_menu.get()

        if not selected:

            messagebox.showwarning(
                "Select Product",
                "Please select a product.",
                parent=window
            )

            return

        try:

            new_stock = float(
                new_stock_entry.get().strip()
            )

            if new_stock < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Stock",
                "Please enter a valid stock quantity.",
                parent=window
            )

            return

        product_id = selected.split(" - ")[0]

        reason = reason_entry.get().strip()

        if not reason:
            reason = "Stock adjustment"

        connection = get_connection()

        try:

            product = connection.execute(
                """
                SELECT stock
                FROM products
                WHERE product_id = ?
                """,
                (product_id,)
            ).fetchone()

            if not product:
                raise Exception("Product not found.")

            stock_before = float(
                product["stock"]
            )

            if new_stock == stock_before:

                messagebox.showwarning(
                    "No Change",
                    "The new stock is the same as the current stock.",
                    parent=window
                )

                connection.close()
                return

            quantity = abs(
                new_stock - stock_before
            )

            connection.execute(
                """
                UPDATE products
                SET stock = ?
                WHERE product_id = ?
                """,
                (
                    new_stock,
                    product_id
                )
            )

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
                    product_id,
                    "ADJUSTMENT",
                    quantity,
                    stock_before,
                    new_stock,
                    reason,
                    "EMP001"
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Stock Adjusted",
                f"Stock adjusted successfully!\n\n"
                f"Previous Stock: {stock_before:g}\n"
                f"New Stock: {new_stock:g}\n"
                f"Difference: {quantity:g}",
                parent=window
            )

            window.destroy()

            if refresh_function:
                refresh_function()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                f"Could not adjust stock.\n\n{error}",
                parent=window
            )

        finally:

            try:
                connection.close()
            except:
                pass

    ctk.CTkButton(
        window,
        text="Save Adjustment",
        width=380,
        height=42,
        fg_color="#5C7A67",
        hover_color="#496453",
        command=save_adjustment
    ).pack(pady=(20, 10))

    ctk.CTkButton(
        window,
        text="Cancel",
        width=380,
        height=40,
        fg_color="#D9E8DE",
        hover_color="#C5D9CC",
        text_color=DARK_GREEN,
        command=window.destroy
    ).pack()


# ============================================================
# Inventory History
# ============================================================

def open_inventory_history(parent_window):

    window = ctk.CTkToplevel(parent_window)

    window.title("GreenTill - Inventory History")
    window.geometry("1050x650")
    window.resizable(False, False)
    window.configure(fg_color=BG)

    window.transient(parent_window)

    ctk.CTkLabel(
        window,
        text="📜 Inventory Transaction History",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        ),
        text_color=DARK_GREEN
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        window,
        text="Complete record of stock additions and adjustments",
        font=ctk.CTkFont(
            size=13
        ),
        text_color=GRAY
    ).pack(pady=(0, 15))

    table_container = ctk.CTkFrame(
        window,
        fg_color=WHITE,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )

    table_container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    table_header = ctk.CTkFrame(
        table_container,
        fg_color="#EAF6EE",
        height=45,
        corner_radius=8
    )

    table_header.pack(
        fill="x",
        padx=8,
        pady=8
    )

    table_header.pack_propagate(False)

    headers = [
        ("ID", 60),
        ("Product", 180),
        ("Type", 120),
        ("Quantity", 90),
        ("Before", 90),
        ("After", 90),
        ("Reason", 190),
        ("Employee", 100)
    ]

    for text, width in headers:

        ctk.CTkLabel(
            table_header,
            text=text,
            width=width,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=DARK_GREEN
        ).pack(
            side="left",
            padx=2
        )

    scroll_frame = ctk.CTkScrollableFrame(
        table_container,
        fg_color="transparent"
    )

    scroll_frame.pack(
        fill="both",
        expand=True,
        padx=8,
        pady=(0, 8)
    )

    connection = None

    try:

        connection = get_connection()

        transactions = connection.execute(
            """
            SELECT
                it.transaction_id,
                p.name AS product_name,
                it.transaction_type,
                it.quantity,
                it.stock_before,
                it.stock_after,
                it.reason,
                COALESCE(e.name, 'System') AS employee_name
            FROM inventory_transactions it
            LEFT JOIN products p
                ON it.product_id = p.product_id
            LEFT JOIN employees e
                ON it.employee_id = e.employee_id
            ORDER BY it.transaction_id DESC
            """
        ).fetchall()

        if not transactions:

            ctk.CTkLabel(
                scroll_frame,
                text="No inventory transactions recorded yet.",
                font=ctk.CTkFont(size=15),
                text_color=GRAY
            ).pack(pady=40)

        else:

            for transaction in transactions:

                row = ctk.CTkFrame(
                    scroll_frame,
                    fg_color="#F9FCFA",
                    corner_radius=8,
                    height=58
                )

                row.pack(
                    fill="x",
                    pady=3
                )

                row.pack_propagate(False)

                ctk.CTkLabel(
                    row,
                    text=str(
                        transaction["transaction_id"]
                    ),
                    width=60
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=transaction["product_name"] or "Unknown",
                    width=180,
                    anchor="w"
                ).pack(side="left", padx=2)

                type_color = (
                    GREEN
                    if transaction["transaction_type"]
                    == "STOCK_IN"
                    else "#B26A00"
                )

                ctk.CTkLabel(
                    row,
                    text=transaction["transaction_type"],
                    width=120,
                    text_color=type_color,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    )
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=f"{float(transaction['quantity']):g}",
                    width=90
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=f"{float(transaction['stock_before']):g}",
                    width=90
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=f"{float(transaction['stock_after']):g}",
                    width=90
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=transaction["reason"] or "-",
                    width=190,
                    anchor="w"
                ).pack(side="left", padx=2)

                ctk.CTkLabel(
                    row,
                    text=transaction["employee_name"] or "System",
                    width=100
                ).pack(side="left", padx=2)

    except Exception as error:

        messagebox.showerror(
            "Database Error",
            f"Unable to load inventory history.\n\n{error}",
            parent=window
        )

    finally:

        if connection:
            connection.close()

    ctk.CTkButton(
        window,
        text="Close",
        width=180,
        height=40,
        fg_color=DARK_GREEN,
        hover_color="#17482D",
        command=window.destroy
    ).pack(pady=(0, 15))


# ============================================================
# Inventory Management Window
# ============================================================

def open_inventory_management():

    inventory_window = ctk.CTkToplevel(dashboard)

    inventory_window.title(
        "GreenTill - Inventory Management"
    )

    inventory_window.geometry(
        "1200x720"
    )

    inventory_window.resizable(
        False,
        False
    )

    inventory_window.configure(
        fg_color=BG
    )

    inventory_window.transient(dashboard)

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    header = ctk.CTkFrame(
        inventory_window,
        fg_color="#EAF6EE",
        corner_radius=15
    )

    header.pack(
        fill="x",
        padx=20,
        pady=(20, 10)
    )

    title_frame = ctk.CTkFrame(
        header,
        fg_color="transparent"
    )

    title_frame.pack(
        side="left",
        padx=20,
        pady=15
    )

    ctk.CTkLabel(
        title_frame,
        text="📦 Inventory Management",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        ),
        text_color=DARK_GREEN
    ).pack(anchor="w")

    ctk.CTkLabel(
        title_frame,
        text=(
            "Manage stock, monitor inventory levels "
            "and track stock changes"
        ),
        font=ctk.CTkFont(size=13),
        text_color="#5B6B62"
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    # --------------------------------------------------------
    # Summary Cards
    # --------------------------------------------------------

    summary_frame = ctk.CTkFrame(
        inventory_window,
        fg_color="transparent"
    )

    summary_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    total_card = ctk.CTkFrame(
        summary_frame,
        fg_color=WHITE,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )

    total_card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 8)
    )

    low_card = ctk.CTkFrame(
        summary_frame,
        fg_color=WHITE,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )

    low_card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8
    )

    out_card = ctk.CTkFrame(
        summary_frame,
        fg_color=WHITE,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )

    out_card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8
    )

    expiry_card = ctk.CTkFrame(
        summary_frame,
        fg_color=WHITE,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )

    expiry_card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(8, 0)
    )

    total_label = ctk.CTkLabel(
        total_card,
        text="Total Products\n0",
        font=ctk.CTkFont(
            size=17,
            weight="bold"
        ),
        text_color=DARK_GREEN
    )

    total_label.pack(pady=18)

    low_label = ctk.CTkLabel(
        low_card,
        text="Low Stock\n0",
        font=ctk.CTkFont(
            size=17,
            weight="bold"
        ),
        text_color="#B26A00"
    )

    low_label.pack(pady=18)

    out_label = ctk.CTkLabel(
        out_card,
        text="Out of Stock\n0",
        font=ctk.CTkFont(
            size=17,
            weight="bold"
        ),
        text_color="#B3261E"
    )

    out_label.pack(pady=18)

    expiry_label = ctk.CTkLabel(
        expiry_card,
        text="Expiry Alerts\n0",
        font=ctk.CTkFont(
            size=17,
            weight="bold"
        ),
        text_color="#B26A00"
    )

    expiry_label.pack(pady=18)

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    filter_frame = ctk.CTkFrame(
        inventory_window,
        fg_color="transparent"
    )

    filter_frame.pack(
        fill="x",
        padx=20,
        pady=(5, 10)
    )

    search_entry = ctk.CTkEntry(
        filter_frame,
        placeholder_text=(
            "Search product name, ID or barcode..."
        ),
        width=300,
        height=38
    )

    search_entry.pack(
        side="left",
        padx=(0, 10)
    )

    category_menu = ctk.CTkOptionMenu(
        filter_frame,
        values=[
            "All Categories",
            "Vegetables",
            "Fruits",
            "Dairy",
            "Grocery",
            "Snacks",
            "Beverages",
            "Personal Care",
            "Household"
        ],
        width=170,
        height=38
    )

    category_menu.pack(
        side="left",
        padx=5
    )

    status_menu = ctk.CTkOptionMenu(
        filter_frame,
        values=[
            "All Status",
            "In Stock",
            "Low Stock",
            "Out of Stock"
        ],
        width=150,
        height=38
    )

    status_menu.pack(
        side="left",
        padx=5
    )

    ctk.CTkButton(
        filter_frame,
        text="📜 Inventory History",
        width=160,
        height=38,
        fg_color=DARK_GREEN,
        hover_color="#17482D",
        command=lambda:
        open_inventory_history(inventory_window)
    ).pack(
        side="right",
        padx=5
    )

    ctk.CTkButton(
        filter_frame,
        text="🔧 Adjust Stock",
        width=130,
        height=38,
        fg_color="#5C7A67",
        hover_color="#496453",
        command=lambda:
        open_adjust_stock(
            inventory_window,
            refresh_function=load_inventory
        )
    ).pack(
        side="right",
        padx=5
    )

    ctk.CTkButton(
        filter_frame,
        text="➕ Add Stock",
        width=120,
        height=38,
        fg_color="#2E7D4F",
        hover_color="#23643F",
        command=lambda:
        open_add_stock(
            inventory_window,
            refresh_function=load_inventory
        )
    ).pack(
        side="right",
        padx=5
    )

    # --------------------------------------------------------
    # Table Container
    # --------------------------------------------------------

    table_container = ctk.CTkFrame(
        inventory_window,
        fg_color=WHITE,
        corner_radius=12,
        border_width=1,
        border_color=BORDER
    )

    table_container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    table_header = ctk.CTkFrame(
        table_container,
        fg_color="#EAF6EE",
        height=45,
        corner_radius=8
    )

    table_header.pack(
        fill="x",
        padx=8,
        pady=8
    )

    table_header.pack_propagate(False)

    headers = [
        ("ID", 80),
        ("Product", 190),
        ("Category", 120),
        ("Unit", 70),
        ("Stock", 90),
        ("Reorder", 90),
        ("Status", 110),
        ("Expiry", 110),
        ("Action", 180)
    ]

    for text, width in headers:

        ctk.CTkLabel(
            table_header,
            text=text,
            width=width,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=DARK_GREEN
        ).pack(
            side="left",
            padx=2
        )

    scroll_frame = ctk.CTkScrollableFrame(
        table_container,
        fg_color="transparent"
    )

    scroll_frame.pack(
        fill="both",
        expand=True,
        padx=8,
        pady=(0, 8)
    )

    # --------------------------------------------------------
    # Load Inventory
    # --------------------------------------------------------

    def load_inventory():

        for widget in scroll_frame.winfo_children():
            widget.destroy()

        connection = None

        try:

            connection = get_connection()

            products = connection.execute(
                """
                SELECT
                    product_id,
                    barcode,
                    name,
                    category,
                    unit,
                    stock,
                    reorder_level,
                    expiry_date
                FROM products
                ORDER BY name
                """
            ).fetchall()

            search_text = (
                search_entry.get()
                .strip()
                .lower()
            )

            selected_category = category_menu.get()
            selected_status = status_menu.get()

            total_products = 0
            low_stock_count = 0
            out_stock_count = 0
            expiry_count = 0

            for product in products:

                stock = float(
                    product["stock"]
                )

                reorder_level = float(
                    product["reorder_level"]
                )

                stock_status = get_stock_status(
                    stock,
                    reorder_level
                )

                # Search
                if search_text:

                    searchable_text = " ".join(
                        [
                            str(product["product_id"]),
                            str(product["barcode"] or ""),
                            str(product["name"])
                        ]
                    ).lower()

                    if search_text not in searchable_text:
                        continue

                # Category
                if (
                    selected_category != "All Categories"
                    and product["category"] != selected_category
                ):
                    continue

                # Status
                if (
                    selected_status != "All Status"
                    and stock_status != selected_status
                ):
                    continue

                total_products += 1

                if stock_status == "Low Stock":
                    low_stock_count += 1

                if stock_status == "Out of Stock":
                    out_stock_count += 1

                expiry_text, expiry_color = get_expiry_status(
                    product["expiry_date"]
                )

                if expiry_text in ["Expired", "Soon"]:
                    expiry_count += 1

                # --------------------------------------------
                # Row
                # --------------------------------------------

                row = ctk.CTkFrame(
                    scroll_frame,
                    fg_color="#F9FCFA",
                    corner_radius=8,
                    height=55
                )

                row.pack(
                    fill="x",
                    pady=3
                )

                row.pack_propagate(False)

                ctk.CTkLabel(
                    row,
                    text=product["product_id"],
                    width=80
                ).pack(
                    side="left",
                    padx=2
                )

                ctk.CTkLabel(
                    row,
                    text=product["name"],
                    width=190,
                    anchor="w",
                    font=ctk.CTkFont(
                        size=11,
                        weight="bold"
                    )
                ).pack(
                    side="left",
                    padx=2
                )

                ctk.CTkLabel(
                    row,
                    text=product["category"],
                    width=120
                ).pack(
                    side="left",
                    padx=2
                )

                ctk.CTkLabel(
                    row,
                    text=product["unit"],
                    width=70
                ).pack(
                    side="left",
                    padx=2
                )

                stock_color = (
                    "#B3261E"
                    if stock <= 0
                    else (
                        "#B26A00"
                        if stock <= reorder_level
                        else GREEN
                    )
                )

                ctk.CTkLabel(
                    row,
                    text=f"{stock:g}",
                    width=90,
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    ),
                    text_color=stock_color
                ).pack(
                    side="left",
                    padx=2
                )

                ctk.CTkLabel(
                    row,
                    text=f"{reorder_level:g}",
                    width=90
                ).pack(
                    side="left",
                    padx=2
                )

                status_color = (
                    GREEN
                    if stock_status == "In Stock"
                    else (
                        "#B26A00"
                        if stock_status == "Low Stock"
                        else "#B3261E"
                    )
                )

                ctk.CTkLabel(
                    row,
                    text=stock_status,
                    width=110,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    ),
                    text_color=status_color
                ).pack(
                    side="left",
                    padx=2
                )

                ctk.CTkLabel(
                    row,
                    text=(
                        product["expiry_date"]
                        if expiry_text in ["Expired", "Soon"]
                        else expiry_text
                    ),
                    width=110,
                    text_color=expiry_color,
                    font=ctk.CTkFont(
                        size=9,
                        weight="bold"
                        if expiry_text in ["Expired", "Soon"]
                        else "normal"
                    )
                ).pack(
                    side="left",
                    padx=2
                )

                action_frame = ctk.CTkFrame(
                    row,
                    fg_color="transparent",
                    width=180
                )

                action_frame.pack(
                    side="left",
                    padx=2
                )

                ctk.CTkButton(
                    action_frame,
                    text="+ Stock",
                    width=75,
                    height=30,
                    fg_color="#2E7D4F",
                    hover_color="#23643F",
                    command=lambda
                    pid=product["product_id"]:
                    open_add_stock(
                        inventory_window,
                        pid,
                        load_inventory
                    )
                ).pack(
                    side="left",
                    padx=3
                )

                ctk.CTkButton(
                    action_frame,
                    text="Adjust",
                    width=75,
                    height=30,
                    fg_color="#5C7A67",
                    hover_color="#496453",
                    command=lambda
                    pid=product["product_id"]:
                    open_adjust_stock(
                        inventory_window,
                        pid,
                        load_inventory
                    )
                ).pack(
                    side="left",
                    padx=3
                )

            # ------------------------------------------------
            # Summary
            # ------------------------------------------------

            total_label.configure(
                text=f"Total Products\n{total_products}"
            )

            low_label.configure(
                text=f"Low Stock\n{low_stock_count}"
            )

            out_label.configure(
                text=f"Out of Stock\n{out_stock_count}"
            )

            expiry_label.configure(
                text=f"Expiry Alerts\n{expiry_count}"
            )

            if total_products == 0:

                ctk.CTkLabel(
                    scroll_frame,
                    text="No inventory items found.",
                    font=ctk.CTkFont(size=15),
                    text_color=GRAY
                ).pack(pady=40)

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load inventory.\n\n{error}",
                parent=inventory_window
            )

        finally:

            if connection:
                connection.close()

    # --------------------------------------------------------
    # Search / Filters
    # --------------------------------------------------------

    search_entry.bind(
        "<KeyRelease>",
        lambda event: load_inventory()
    )

    category_menu.configure(
        command=lambda value:
        load_inventory()
    )

    status_menu.configure(
        command=lambda value:
        load_inventory()
    )

    # Initial load
    load_inventory()


# ============================================================
# Sidebar Navigation Functions
# ============================================================

def show_dashboard():
    dashboard.deiconify()
    dashboard.lift()


def show_employees():
    open_employee_management()


def show_products():
    open_product_management()


def show_inventory():
    open_inventory_management()


def show_bills():
    """Admin bill history."""
    bill_window = ctk.CTkToplevel(dashboard)
    bill_window.title("GreenTill - Bill History")
    bill_window.geometry("1100x650")
    bill_window.minsize(950, 550)
    bill_window.configure(fg_color=BG)
    bill_window.transient(dashboard)

    header = ctk.CTkFrame(bill_window, height=90, fg_color=WHITE,
                          corner_radius=0, border_width=1,
                          border_color=BORDER)
    header.pack(fill="x")
    header.pack_propagate(False)
    ctk.CTkLabel(header, text="🧾  Bill History",
                 font=ctk.CTkFont(size=24, weight="bold"),
                 text_color=TEXT).pack(side="left", padx=30)

    body = ctk.CTkFrame(bill_window, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=25, pady=20)

    table = ctk.CTkScrollableFrame(body, fg_color=WHITE, corner_radius=12)
    table.pack(fill="both", expand=True)

    columns = [("Bill ID",120),("Date",110),("Time",100),("Employee",180),
               ("Customer",150),("Amount",120),("Payment",100),("Status",100)]
    head = ctk.CTkFrame(table, fg_color="#E8F5EC", height=42, corner_radius=6)
    head.pack(fill="x", padx=8, pady=8)
    head.pack_propagate(False)
    for text, width in columns:
        ctk.CTkLabel(head, text=text, width=width,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=GREEN).pack(side="left", padx=2)

    try:
        con=get_connection()
        rows=con.execute("""
            SELECT b.bill_id,b.bill_date,b.bill_time,b.employee_id,
                   COALESCE(e.name,'-') employee_name,
                   COALESCE(b.customer_id,'Guest') customer_id,
                   b.total_amount,b.payment_method,b.bill_status
            FROM bills b LEFT JOIN employees e ON b.employee_id=e.employee_id
            ORDER BY b.bill_date DESC,b.bill_time DESC
        """).fetchall()
        con.close()
        if not rows:
            ctk.CTkLabel(table,text="No bills found.",font=ctk.CTkFont(size=15),
                         text_color=GRAY).pack(pady=40)
        else:
            for bill in rows:
                row=ctk.CTkFrame(table,fg_color=WHITE,height=44,corner_radius=6)
                row.pack(fill="x",padx=8,pady=3); row.pack_propagate(False)
                vals=[bill["bill_id"],bill["bill_date"],bill["bill_time"],
                      bill["employee_name"],bill["customer_id"] or "Guest",
                      f"₹{float(bill['total_amount']):.2f}",bill["payment_method"] or "-",
                      bill["bill_status"] or "-"]
                for value,(_,width) in zip(vals,columns):
                    ctk.CTkLabel(row,text=str(value),width=width,anchor="center").pack(side="left",padx=2)
    except Exception as error:
        messagebox.showerror("Bill History", f"Unable to load bills.\n\n{error}", parent=bill_window)


def show_analytics():
    """Admin sales analytics based on completed bills."""
    win=ctk.CTkToplevel(dashboard)
    win.title("GreenTill - Sales Analytics")
    win.geometry("1050x650")
    win.configure(fg_color=BG)
    win.transient(dashboard)

    ctk.CTkLabel(win,text="📊  Sales Analytics",
                 font=ctk.CTkFont(size=24,weight="bold"),text_color=TEXT).pack(anchor="w",padx=30,pady=(25,5))
    ctk.CTkLabel(win,text="Overview of completed supermarket sales",text_color=GRAY).pack(anchor="w",padx=30)

    try:
        con=get_connection()
        total=con.execute("SELECT COALESCE(SUM(total_amount),0) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID'").fetchone()["v"]
        count=con.execute("SELECT COUNT(*) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID'").fetchone()["v"]
        today=con.execute("SELECT COALESCE(SUM(total_amount),0) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID' AND bill_date=DATE('now')").fetchone()["v"]
        today_count=con.execute("SELECT COUNT(*) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID' AND bill_date=DATE('now')").fetchone()["v"]
        avg=(float(total)/count) if count else 0
        methods=con.execute("SELECT COALESCE(payment_method,'Unknown') method,COUNT(*) cnt,COALESCE(SUM(total_amount),0) amount FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID' GROUP BY payment_method ORDER BY amount DESC").fetchall()
        con.close()
    except Exception as error:
        messagebox.showerror("Sales Analytics",f"Unable to calculate analytics.\n\n{error}",parent=win); return

    cards=ctk.CTkFrame(win,fg_color="transparent"); cards.pack(fill="x",padx=30,pady=25)
    for title,value,sub in [("Total Sales",f"₹{float(total):,.2f}",f"{count} completed bills"),
                            ("Today's Sales",f"₹{float(today):,.2f}",f"{today_count} bills today"),
                            ("Average Bill",f"₹{avg:,.2f}","Per completed bill")]:
        card=ctk.CTkFrame(cards,width=300,height=125,fg_color=WHITE,corner_radius=16,border_width=1,border_color=BORDER)
        card.pack(side="left",fill="both",expand=True,padx=(0,12)); card.pack_propagate(False)
        ctk.CTkLabel(card,text=title,font=ctk.CTkFont(size=13,weight="bold"),text_color=GRAY).pack(anchor="w",padx=20,pady=(18,5))
        ctk.CTkLabel(card,text=value,font=ctk.CTkFont(size=25,weight="bold"),text_color=TEXT).pack(anchor="w",padx=20)
        ctk.CTkLabel(card,text=sub,font=ctk.CTkFont(size=11),text_color=GRAY).pack(anchor="w",padx=20)

    method_card=ctk.CTkFrame(win,fg_color=WHITE,corner_radius=16,border_width=1,border_color=BORDER)
    method_card.pack(fill="both",expand=True,padx=30,pady=(0,25))
    ctk.CTkLabel(method_card,text="Payment Method Breakdown",font=ctk.CTkFont(size=18,weight="bold"),text_color=TEXT).pack(anchor="w",padx=20,pady=15)
    for rowdata in methods:
        line=ctk.CTkFrame(method_card,fg_color="#F5FAF6",corner_radius=8); line.pack(fill="x",padx=20,pady=4)
        ctk.CTkLabel(line,text=str(rowdata["method"]),width=180,anchor="w").pack(side="left",padx=12,pady=10)
        ctk.CTkLabel(line,text=f"{rowdata['cnt']} bills",width=130).pack(side="left")
        ctk.CTkLabel(line,text=f"₹{float(rowdata['amount']):,.2f}",width=150,font=ctk.CTkFont(weight="bold"),text_color=GREEN).pack(side="right",padx=12)


def show_eco():
    """Store sustainability dashboard."""
    win=ctk.CTkToplevel(dashboard)
    win.title("GreenTill - Eco Dashboard")
    win.geometry("950x600")
    win.configure(fg_color=BG); win.transient(dashboard)
    ctk.CTkLabel(win,text="🌱  Eco Dashboard",font=ctk.CTkFont(size=24,weight="bold"),text_color=DARK_GREEN).pack(anchor="w",padx=30,pady=(25,5))
    ctk.CTkLabel(win,text="Sustainability statistics calculated from completed bills",text_color=GRAY).pack(anchor="w",padx=30)
    try:
        con=get_connection()
        points=con.execute("SELECT COALESCE(SUM(eco_points),0) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID'").fetchone()["v"]
        eco_bills=con.execute("SELECT COUNT(*) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID' AND COALESCE(eco_score,0)>0").fetchone()["v"]
        avg_score=con.execute("SELECT COALESCE(AVG(eco_score),0) v FROM bills WHERE bill_status='COMPLETED' AND payment_status='PAID'").fetchone()["v"]
        con.close()
    except Exception as error:
        messagebox.showerror("Eco Dashboard",f"Unable to load eco data.\n\n{error}",parent=win); return
    grid=ctk.CTkFrame(win,fg_color="transparent"); grid.pack(fill="x",padx=30,pady=30)
    for title,value,desc in [("Eco Points Generated",str(int(points)),"Across completed bills"),
                             ("Eco-Friendly Bills",str(eco_bills),"Bills with an eco score"),
                             ("Average Eco Score",f"{float(avg_score):.1f}/100","Completed bills")]:
        card=ctk.CTkFrame(grid,fg_color="#ECF8EF",corner_radius=16,border_width=1,border_color=BORDER,height=145)
        card.pack(side="left",fill="both",expand=True,padx=6); card.pack_propagate(False)
        ctk.CTkLabel(card,text=title,font=ctk.CTkFont(size=13,weight="bold"),text_color=GRAY).pack(anchor="w",padx=20,pady=(20,5))
        ctk.CTkLabel(card,text=value,font=ctk.CTkFont(size=28,weight="bold"),text_color=DARK_GREEN).pack(anchor="w",padx=20)
        ctk.CTkLabel(card,text=desc,font=ctk.CTkFont(size=11),text_color=GRAY).pack(anchor="w",padx=20)
    note=ctk.CTkFrame(win,fg_color=WHITE,corner_radius=14,border_width=1,border_color=BORDER); note.pack(fill="both",expand=True,padx=30,pady=(0,30))
    ctk.CTkLabel(note,text="About GreenTill Eco Tracking",font=ctk.CTkFont(size=18,weight="bold"),text_color=TEXT).pack(anchor="w",padx=22,pady=(20,8))
    ctk.CTkLabel(note,text="Eco Points and Eco Scores are based on the product data entered in GreenTill.\nEnvironmental impact figures are estimates for store-level tracking, not exact measurements.",justify="left",text_color=GRAY).pack(anchor="w",padx=22)


def show_settings():
    """GreenTill application settings."""
    win=ctk.CTkToplevel(dashboard)
    win.title("GreenTill - Settings")
    win.geometry("700x520")
    win.configure(fg_color=BG); win.transient(dashboard)
    ctk.CTkLabel(win,text="⚙  Settings",font=ctk.CTkFont(size=24,weight="bold"),text_color=TEXT).pack(anchor="w",padx=30,pady=(25,5))
    ctk.CTkLabel(win,text="Application and store configuration",text_color=GRAY).pack(anchor="w",padx=30,pady=(0,20))
    frame=ctk.CTkFrame(win,fg_color=WHITE,corner_radius=14,border_width=1,border_color=BORDER); frame.pack(fill="both",expand=True,padx=30,pady=(0,30))
    ctk.CTkLabel(frame,text="Store Information",font=ctk.CTkFont(size=17,weight="bold"),text_color=TEXT).pack(anchor="w",padx=22,pady=(20,12))
    for label,default in [("Store Name","GreenTill Supermarket"),("UPI ID","greentillstore@upi")]:
        ctk.CTkLabel(frame,text=label,font=ctk.CTkFont(size=12,weight="bold"),text_color=GRAY).pack(anchor="w",padx=22,pady=(8,3))
        entry=ctk.CTkEntry(frame,height=38); entry.insert(0,default); entry.pack(fill="x",padx=22)
    ctk.CTkLabel(frame,text="Receipt phone numbers are not printed; customer details are optional.",text_color=GRAY,font=ctk.CTkFont(size=11)).pack(anchor="w",padx=22,pady=18)
    ctk.CTkButton(frame,text="SAVE SETTINGS",height=40,fg_color=GREEN,hover_color=GREEN_HOVER,command=lambda: messagebox.showinfo("Settings","Settings saved for this session.",parent=win)).pack(anchor="e",padx=22,pady=15)


# ============================================================
# Sidebar
# ============================================================

sidebar = ctk.CTkFrame(
    dashboard,
    width=250,
    height=760,
    corner_radius=0,
    fg_color=SIDEBAR
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ============================================================
# Sidebar Logo
# ============================================================

logo_frame = ctk.CTkFrame(
    sidebar,
    fg_color="transparent"
)

logo_frame.pack(
    fill="x",
    padx=25,
    pady=(30, 5)
)

ctk.CTkLabel(
    logo_frame,
    text="🌿",
    font=ctk.CTkFont(size=30),
    text_color=WHITE
).pack(side="left")

ctk.CTkLabel(
    logo_frame,
    text="GreenTill",
    font=ctk.CTkFont(
        family="Arial",
        size=26,
        weight="bold"
    ),
    text_color=WHITE
).pack(
    side="left",
    padx=(8, 0)
)


# ============================================================
# Tagline
# ============================================================

ctk.CTkLabel(
    sidebar,
    text="Smart Billing.\nGreener Shopping.",
    font=ctk.CTkFont(
        family="Arial",
        size=12
    ),
    text_color="#B8DCC8",
    justify="left"
).pack(
    anchor="w",
    padx=58,
    pady=(0, 35)
)


ctk.CTkLabel(
    sidebar,
    text="MAIN MENU",
    font=ctk.CTkFont(
        family="Arial",
        size=11,
        weight="bold"
    ),
    text_color="#7FAF92"
).pack(
    anchor="w",
    padx=28,
    pady=(0, 10)
)


# ============================================================
# Sidebar Button Helper
# ============================================================

def create_sidebar_button(
    text,
    command
):

    button = ctk.CTkButton(
        sidebar,
        text=text,
        height=45,
        corner_radius=10,
        fg_color="transparent",
        hover_color=SIDEBAR_HOVER,
        text_color="#E9F5EE",
        anchor="w",
        font=ctk.CTkFont(
            family="Arial",
            size=14
        ),
        command=command
    )

    button.pack(
        fill="x",
        padx=15,
        pady=3
    )

    return button


# ============================================================
# Navigation Buttons
# ============================================================

create_sidebar_button(
    "  🏠   Dashboard",
    show_dashboard
)

create_sidebar_button(
    "  👥   Employees",
    show_employees
)

create_sidebar_button(
    "  📦   Products",
    show_products
)

create_sidebar_button(
    "  🏪   Inventory",
    show_inventory
)

create_sidebar_button(
    "  🧾   Bills",
    show_bills
)

create_sidebar_button(
    "  📊   Sales Analytics",
    show_analytics
)

create_sidebar_button(
    "  🌱   Eco Dashboard",
    show_eco
)


# ============================================================
# Bottom Sidebar
# ============================================================

bottom_frame = ctk.CTkFrame(
    sidebar,
    fg_color="transparent"
)

bottom_frame.pack(
    side="bottom",
    fill="x",
    padx=15,
    pady=20
)


def logout():

    dashboard.destroy()


ctk.CTkButton(
    bottom_frame,
    text="  ⚙   Settings",
    height=43,
    corner_radius=10,
    fg_color="transparent",
    hover_color=SIDEBAR_HOVER,
    text_color="#E9F5EE",
    anchor="w",
    font=ctk.CTkFont(
        family="Arial",
        size=14
    ),
    command=show_settings
).pack(
    fill="x",
    pady=3
)


ctk.CTkButton(
    bottom_frame,
    text="  🚪   Logout",
    height=43,
    corner_radius=10,
    fg_color="#A83D3D",
    hover_color="#8F3030",
    text_color=WHITE,
    anchor="w",
    font=ctk.CTkFont(
        family="Arial",
        size=14,
        weight="bold"
    ),
    command=logout
).pack(
    fill="x",
    pady=3
)


# ============================================================
# Main Content Area
# ============================================================

content_area = ctk.CTkFrame(
    dashboard,
    fg_color=BG,
    corner_radius=0
)

content_area.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# Top Header
# ============================================================

header = ctk.CTkFrame(
    content_area,
    height=85,
    fg_color=WHITE,
    corner_radius=0,
    border_width=1,
    border_color=BORDER
)

header.pack(fill="x")
header.pack_propagate(False)


header_left = ctk.CTkFrame(
    header,
    fg_color="transparent"
)

header_left.pack(
    side="left",
    padx=30
)

ctk.CTkLabel(
    header_left,
    text="Admin Dashboard",
    font=ctk.CTkFont(
        family="Arial",
        size=24,
        weight="bold"
    ),
    text_color=TEXT
).pack(anchor="w")

ctk.CTkLabel(
    header_left,
    text="Manage your GreenTill supermarket",
    font=ctk.CTkFont(
        family="Arial",
        size=12
    ),
    text_color=GRAY
).pack(
    anchor="w",
    pady=(2, 0)
)


# ============================================================
# Admin Profile
# ============================================================

profile = ctk.CTkFrame(
    header,
    fg_color="#F0F8F2",
    corner_radius=12
)

profile.pack(
    side="right",
    padx=25
)

ctk.CTkLabel(
    profile,
    text="👑",
    font=ctk.CTkFont(size=22)
).pack(
    side="left",
    padx=(12, 5),
    pady=8
)

profile_text = ctk.CTkFrame(
    profile,
    fg_color="transparent"
)

profile_text.pack(
    side="left",
    padx=(0, 14)
)

ctk.CTkLabel(
    profile_text,
    text="GreenTill Admin",
    font=ctk.CTkFont(
        size=13,
        weight="bold"
    ),
    text_color=TEXT
).pack(anchor="w")

ctk.CTkLabel(
    profile_text,
    text="Administrator",
    font=ctk.CTkFont(size=11),
    text_color=GRAY
).pack(anchor="w")


# ============================================================
# Welcome Section
# ============================================================

welcome = ctk.CTkFrame(
    content_area,
    fg_color="transparent"
)

welcome.pack(
    fill="x",
    padx=30,
    pady=(28, 20)
)

ctk.CTkLabel(
    welcome,
    text="Good Morning, Admin 🌿",
    font=ctk.CTkFont(
        family="Arial",
        size=28,
        weight="bold"
    ),
    text_color=TEXT
).pack(anchor="w")

ctk.CTkLabel(
    welcome,
    text="Here's an overview of your supermarket today.",
    font=ctk.CTkFont(
        family="Arial",
        size=14
    ),
    text_color=GRAY
).pack(
    anchor="w",
    pady=(5, 0)
)


# ============================================================
# Statistics Cards
# ============================================================

stats_frame = ctk.CTkFrame(
    content_area,
    fg_color="transparent"
)

stats_frame.pack(
    fill="x",
    padx=30
)


def create_stat_card(
    parent,
    icon,
    title,
    value,
    subtitle
):

    card = ctk.CTkFrame(
        parent,
        width=215,
        height=125,
        corner_radius=18,
        fg_color=WHITE,
        border_width=1,
        border_color=BORDER
    )

    card.pack(
        side="left",
        padx=(0, 15)
    )

    card.pack_propagate(False)

    top = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    top.pack(
        fill="x",
        padx=18,
        pady=(15, 5)
    )

    ctk.CTkLabel(
        top,
        text=icon,
        font=ctk.CTkFont(size=23)
    ).pack(side="left")

    ctk.CTkLabel(
        top,
        text=title,
        font=ctk.CTkFont(
            size=12,
            weight="bold"
        ),
        text_color=GRAY
    ).pack(
        side="left",
        padx=8
    )

    ctk.CTkLabel(
        card,
        text=value,
        font=ctk.CTkFont(
            size=25,
            weight="bold"
        ),
        text_color=TEXT
    ).pack(
        anchor="w",
        padx=18
    )

    ctk.CTkLabel(
        card,
        text=subtitle,
        font=ctk.CTkFont(size=10),
        text_color=GRAY
    ).pack(
        anchor="w",
        padx=18
    )


create_stat_card(
    stats_frame,
    "₹",
    "Today's Sales",
    "₹0.00",
    "No sales yet"
)

create_stat_card(
    stats_frame,
    "🧾",
    "Bills",
    "0",
    "Completed bills"
)

create_stat_card(
    stats_frame,
    "📦",
    "Products",
    "0",
    "Products in system"
)

create_stat_card(
    stats_frame,
    "⚠",
    "Low Stock",
    "0",
    "Items need attention"
)


# ============================================================
# Bottom Dashboard Sections
# ============================================================

bottom_content = ctk.CTkFrame(
    content_area,
    fg_color="transparent"
)

bottom_content.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


# ============================================================
# Recent Activity
# ============================================================

activity_card = ctk.CTkFrame(
    bottom_content,
    width=440,
    height=280,
    corner_radius=18,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER
)

activity_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 12)
)

activity_card.pack_propagate(False)

ctk.CTkLabel(
    activity_card,
    text="Recent Activity",
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    ),
    text_color=TEXT
).pack(
    anchor="w",
    padx=22,
    pady=(20, 3)
)

ctk.CTkLabel(
    activity_card,
    text="Your latest store activities will appear here.",
    font=ctk.CTkFont(size=12),
    text_color=GRAY
).pack(
    anchor="w",
    padx=22
)

ctk.CTkLabel(
    activity_card,
    text="🌿\n\nNo recent activity",
    font=ctk.CTkFont(size=14),
    text_color="#91A099",
    justify="center"
).pack(expand=True)


# ============================================================
# Eco Overview
# ============================================================

eco_card = ctk.CTkFrame(
    bottom_content,
    width=440,
    height=280,
    corner_radius=18,
    fg_color="#ECF8EF",
    border_width=1,
    border_color=BORDER
)

eco_card.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(12, 0)
)

eco_card.pack_propagate(False)

ctk.CTkLabel(
    eco_card,
    text="🌱  Eco Overview",
    font=ctk.CTkFont(
        size=18,
        weight="bold"
    ),
    text_color=DARK_GREEN
).pack(
    anchor="w",
    padx=22,
    pady=(20, 5)
)

ctk.CTkLabel(
    eco_card,
    text="Track the environmental impact of your store.",
    font=ctk.CTkFont(size=12),
    text_color=GRAY
).pack(
    anchor="w",
    padx=22
)


eco_info = ctk.CTkFrame(
    eco_card,
    fg_color="transparent"
)

eco_info.pack(
    fill="x",
    padx=22,
    pady=25
)


def eco_item(title, value):

    frame = ctk.CTkFrame(
        eco_info,
        fg_color=WHITE,
        corner_radius=12
    )

    frame.pack(
        fill="x",
        pady=5
    )

    ctk.CTkLabel(
        frame,
        text=title,
        font=ctk.CTkFont(size=12),
        text_color=GRAY
    ).pack(
        side="left",
        padx=15,
        pady=10
    )

    ctk.CTkLabel(
        frame,
        text=value,
        font=ctk.CTkFont(
            size=13,
            weight="bold"
        ),
        text_color=DARK_GREEN
    ).pack(
        side="right",
        padx=15
    )


eco_item(
    "Eco Points Generated",
    "0"
)

eco_item(
    "Eco-Friendly Bills",
    "0"
)


# ============================================================
# Public entry point
# ============================================================

def open_admin_dashboard():
    dashboard.deiconify()
    dashboard.lift()
    dashboard.focus_force()
    dashboard.mainloop()


# ============================================================
# Start Dashboard
# ============================================================

if __name__ == "__main__":

    dashboard.mainloop()