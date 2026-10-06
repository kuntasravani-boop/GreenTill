import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from pathlib import Path
from database import authenticate_user


# ============================================================
# GreenTill - Smart Supermarket POS
# Login Screen
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#F4FAF3"
CARD_COLOR = "#FFFFFF"

GREEN = "#249E59"
GREEN_HOVER = "#1D874B"

DARK_GREEN = "#075B43"
TEXT_DARK = "#17332B"
TEXT_GRAY = "#71847D"

BORDER_COLOR = "#DCE8E2"


# ============================================================
# MAIN WINDOW
# ============================================================

login_window = ctk.CTk()

login_window.title(
    "GreenTill - Smart Supermarket POS"
)

login_window.geometry(
    "1280x800"
)

login_window.minsize(
    1100,
    700
)

login_window.configure(
    fg_color=BG_COLOR
)


# ============================================================
# MAIN CONTAINER
# ============================================================

main_container = ctk.CTkFrame(
    login_window,
    fg_color=BG_COLOR,
    corner_radius=0
)

main_container.pack(
    fill="both",
    expand=True
)


# ============================================================
# LEFT BRANDING SECTION
# ============================================================

left_frame = ctk.CTkFrame(
    main_container,
    fg_color=BG_COLOR,
    corner_radius=0
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(35, 0),
    pady=30
)


# ------------------------------------------------------------
# Branding Image
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

branding_path = BASE_DIR / "assets" / "green_branding.png"

try:

    branding_image = Image.open(branding_path)

    branding_ctk_image = ctk.CTkImage(
        light_image=branding_image,
        dark_image=branding_image,
        size=(600, 740)
    )

    branding_label = ctk.CTkLabel(
        left_frame,
        image=branding_ctk_image,
        text=""
    )

    branding_label.pack(
        fill="both",
        expand=True
    )

except Exception:

    # Fallback if branding image is not found
    branding_label = ctk.CTkLabel(
        left_frame,
        text=(
            "GreenTill\n\n"
            "Smart Billing. Greener Shopping.\n\n"
            "Smart POS  •  Inventory  •  Analytics  •  Eco Tracking"
        ),
        text_color=DARK_GREEN,
        font=ctk.CTkFont(
            family="Arial",
            size=24,
            weight="bold"
        ),
        justify="center"
    )

    branding_label.pack(
        fill="both",
        expand=True
    )


# ============================================================
# RIGHT SECTION
# ============================================================

right_frame = ctk.CTkFrame(
    main_container,
    fg_color=BG_COLOR,
    corner_radius=0
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(25, 35),
    pady=30
)


# ============================================================
# TOP RIGHT MESSAGE
# ============================================================

top_message_frame = ctk.CTkFrame(
    right_frame,
    fg_color="transparent"
)

top_message_frame.pack(
    fill="x",
    pady=(0, 25)
)


top_icon = ctk.CTkLabel(
    top_message_frame,
    text="◉",
    text_color=GREEN,
    font=ctk.CTkFont(
        family="Arial",
        size=25
    )
)

top_icon.pack(
    side="left",
    padx=(0, 10)
)


top_message = ctk.CTkLabel(
    top_message_frame,
    text="A Greener Tomorrow\nStarts at Your Checkout",
    text_color=DARK_GREEN,
    font=ctk.CTkFont(
        family="Arial",
        size=16,
        weight="bold"
    ),
    justify="left"
)

top_message.pack(
    side="left"
)


# ============================================================
# LOGIN CARD
# ============================================================

login_card = ctk.CTkFrame(
    right_frame,
    fg_color=CARD_COLOR,
    corner_radius=25,
    border_width=1,
    border_color="#E1EBE5"
)

login_card.pack(
    fill="both",
    expand=True
)


# ============================================================
# LOGIN CARD CONTENT
# ============================================================

card_content = ctk.CTkFrame(
    login_card,
    fg_color="transparent"
)

card_content.pack(
    fill="both",
    expand=True,
    padx=60,
    pady=45
)


# ============================================================
# WELCOME BACK
# ============================================================

welcome_frame = ctk.CTkFrame(
    card_content,
    fg_color="transparent"
)

welcome_frame.pack(
    pady=(0, 5)
)


welcome_label = ctk.CTkLabel(
    welcome_frame,
    text="Welcome Back",
    text_color=TEXT_DARK,
    font=ctk.CTkFont(
        family="Arial",
        size=32,
        weight="bold"
    )
)

welcome_label.pack(
    side="left"
)


welcome_leaf = ctk.CTkLabel(
    welcome_frame,
    text="♨",
    text_color=DARK_GREEN,
    font=ctk.CTkFont(
        family="Arial",
        size=24
    )
)

welcome_leaf.pack(
    side="left",
    padx=(12, 0)
)


# ============================================================
# SUBTITLE
# ============================================================

subtitle = ctk.CTkLabel(
    card_content,
    text="Sign in to continue to GreenTill",
    text_color=TEXT_GRAY,
    font=ctk.CTkFont(
        family="Arial",
        size=15
    )
)

subtitle.pack(
    pady=(0, 42)
)


# ============================================================
# USERNAME LABEL
# ============================================================

username_label = ctk.CTkLabel(
    card_content,
    text="Username",
    text_color=TEXT_DARK,
    font=ctk.CTkFont(
        family="Arial",
        size=15,
        weight="bold"
    ),
    anchor="w"
)

username_label.pack(
    fill="x",
    pady=(0, 8)
)


# ============================================================
# USERNAME ENTRY
# ============================================================

username_entry = ctk.CTkEntry(
    card_content,
    height=52,
    corner_radius=12,
    border_width=1,
    border_color=BORDER_COLOR,
    fg_color="#FCFEFD",
    text_color=TEXT_DARK,
    placeholder_text="Enter username",
    placeholder_text_color="#A2B1AB",
    font=ctk.CTkFont(
        family="Arial",
        size=15
    )
)

username_entry.pack(
    fill="x",
    pady=(0, 28)
)


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = ctk.CTkLabel(
    card_content,
    text="Password",
    text_color=TEXT_DARK,
    font=ctk.CTkFont(
        family="Arial",
        size=15,
        weight="bold"
    ),
    anchor="w"
)

password_label.pack(
    fill="x",
    pady=(0, 8)
)


# ============================================================
# PASSWORD FRAME
# ============================================================

password_frame = ctk.CTkFrame(
    card_content,
    fg_color="#FCFEFD",
    corner_radius=12,
    border_width=1,
    border_color=BORDER_COLOR,
    height=52
)

password_frame.pack(
    fill="x"
)

password_frame.pack_propagate(False)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = ctk.CTkEntry(
    password_frame,
    height=50,
    corner_radius=12,
    border_width=0,
    fg_color="transparent",
    text_color=TEXT_DARK,
    placeholder_text="Enter password",
    placeholder_text_color="#A2B1AB",
    show="*",
    font=ctk.CTkFont(
        family="Arial",
        size=15
    )
)

password_entry.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(12, 0)
)


# ============================================================
# PASSWORD SHOW / HIDE
# ============================================================

password_visible = False


def toggle_password():

    global password_visible

    if password_visible:

        password_entry.configure(
            show="*"
        )

        password_visible = False

    else:

        password_entry.configure(
            show=""
        )

        password_visible = True


password_eye_button = ctk.CTkButton(
    password_frame,
    text="◉",
    width=45,
    height=45,
    fg_color="transparent",
    hover_color="#F0F5F2",
    text_color="#80938C",
    font=ctk.CTkFont(
        family="Arial",
        size=15
    ),
    command=toggle_password
)

password_eye_button.pack(
    side="right",
    padx=4
)


# ============================================================
# REMEMBER ME / FORGOT PASSWORD
# ============================================================

options_frame = ctk.CTkFrame(
    card_content,
    fg_color="transparent"
)

options_frame.pack(
    fill="x",
    pady=(20, 30)
)


remember_var = ctk.BooleanVar(
    value=False
)


remember_checkbox = ctk.CTkCheckBox(
    options_frame,
    text="Remember me",
    variable=remember_var,
    text_color=TEXT_GRAY,
    fg_color=GREEN,
    hover_color=GREEN_HOVER,
    border_color="#B8D3C5",
    font=ctk.CTkFont(
        family="Arial",
        size=14
    )
)

remember_checkbox.pack(
    side="left"
)


def forgot_password():

    messagebox.showinfo(
        "Forgot Password",
        "Please contact the GreenTill administrator to reset your password."
    )


forgot_button = ctk.CTkButton(
    options_frame,
    text="Forgot Password?",
    width=130,
    height=30,
    fg_color="transparent",
    hover_color="#F1F8F3",
    text_color=GREEN,
    font=ctk.CTkFont(
        family="Arial",
        size=14,
        weight="bold"
    ),
    command=forgot_password
)

forgot_button.pack(
    side="right"
)


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # ========================================================
    # CHECK EMPTY FIELDS
    # ========================================================

    if username == "" or password == "":

        messagebox.showwarning(
            "Login Required",
            "Please enter username and password."
        )

        return


    # ========================================================
    # DATABASE AUTHENTICATION
    # ========================================================

    user = authenticate_user(
        username,
        password
    )


    # ========================================================
    # INVALID LOGIN
    # ========================================================

    if user is None:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )

        return


    # ========================================================
    # GET USER ROLE
    # ========================================================

    role = user["role"]

    employee_id = user["employee_id"]

    employee_name = user["name"]

    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    if role == "Admin":

        try:

            # Load dashboard while login is still visible.
            import admin_dashboard

            dashboard = admin_dashboard.dashboard

            # Prepare dashboard before switching windows.
            dashboard.update_idletasks()
            dashboard.deiconify()
            dashboard.update_idletasks()
            dashboard.lift()
            dashboard.focus_force()

            # Switch only after dashboard is ready.
            login_window.withdraw()

        except Exception as error:

            messagebox.showerror(
                "Admin Dashboard Error",
                f"Unable to open Admin Dashboard.\n\n{error}"
            )

        return


    # ========================================================
    # EMPLOYEE LOGIN
    # ========================================================

    elif role == "Employee":

        try:

            # Load billing while login is still visible.
            import employee_billing

            employee_billing.CURRENT_EMPLOYEE_ID = employee_id

            billing_window = employee_billing.billing_window

            # Prepare billing before switching windows.
            billing_window.update_idletasks()
            billing_window.deiconify()
            billing_window.update_idletasks()
            billing_window.lift()
            billing_window.focus_force()

            # Switch only after billing is ready.
            login_window.withdraw()

        except Exception as error:

            messagebox.showerror(
                "Employee Dashboard Error",
                f"Unable to open Employee Dashboard.\n\n{error}"
            )

        return


    # ========================================================
    # UNKNOWN ROLE
    # ========================================================

    else:

        messagebox.showerror(
            "Login Failed",
            f"Unsupported user role: {role}"
        )

        return


# ============================================================
# LOGIN BUTTON
# ============================================================

login_button = ctk.CTkButton(
    card_content,
    text="↪  LOGIN",
    height=55,
    corner_radius=13,
    fg_color=GREEN,
    hover_color=GREEN_HOVER,
    text_color=WHITE if False else "#FFFFFF",
    font=ctk.CTkFont(
        family="Arial",
        size=17,
        weight="bold"
    ),
    command=login
)

login_button.pack(
    fill="x"
)


# ============================================================
# FOOTER
# ============================================================

footer_label = ctk.CTkLabel(
    card_content,
    text="GreenTill POS System",
    text_color="#91A49D",
    font=ctk.CTkFont(
        family="Arial",
        size=12
    )
)

footer_label.pack(
    side="bottom",
    pady=(20, 0)
)


# ============================================================
# ENTER KEY
# ============================================================

login_window.bind(
    "<Return>",
    lambda event: login()
)


# ============================================================
# FOCUS USERNAME
# ============================================================

username_entry.focus()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    login_window.mainloop()