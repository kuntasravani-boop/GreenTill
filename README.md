
# 🌱 GreenTill — Smart Billing. Greener Shopping.

GreenTill is a **Python-based supermarket Point of Sale (POS) and management system** designed to simplify billing, inventory management, customer management, sales tracking, and sustainability-focused analytics.

The system provides separate workflows for **Administrators and Employees/Cashiers**, with SQLite used for local data management.

---

## 📌 Project Overview

GreenTill is designed as a complete supermarket management application that combines everyday POS operations with sustainability-oriented features.

### Main capabilities

- 🧾 Supermarket billing and checkout
- 📦 Product and inventory management
- 👥 Employee management
- 👤 Customer management
- 📷 Barcode scanning
- 💳 Payment processing
- 🧾 PDF receipt generation
- 📊 Sales analytics
- 🌱 Eco Score and Eco Points
- 📈 Admin dashboard
- ⚠️ Low-stock monitoring
- 🔄 Automatic inventory updates after completed sales
- 🕒 Customer billing history

---

## 🎯 Objectives

The main objectives of GreenTill are to:

1. Automate supermarket billing operations.
2. Maintain product and inventory information efficiently.
3. Reduce manual errors during checkout.
4. Provide administrators with useful sales and inventory insights.
5. Maintain customer purchase history.
6. Support barcode-based product lookup.
7. Generate digital PDF receipts.
8. Introduce sustainability-focused metrics through Eco Score and Eco Points.
9. Provide separate functionality for administrators and employees.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application development |
| **CustomTkinter** | Desktop GUI |
| **SQLite** | Database management |
| **OpenCV** | Barcode camera/scanning |
| **Pyzbar** | Barcode decoding |
| **Pillow** | Image handling |
| **ReportLab** | PDF receipt generation |
| **Matplotlib** | Sales visualization |
| **QRCode** | UPI payment QR generation |
| **Git & GitHub** | Version control and project hosting |

---

## 👥 User Roles

### 👨‍💼 Administrator

The Admin dashboard provides access to:

- Employee Management
- Product Management
- Inventory Management
- Bill History
- Sales Analytics
- Eco Dashboard
- Customer information
- System settings
- Dashboard statistics

### 🧑‍💻 Employee / Cashier

Employees can:

- Log in
- Start a billing shift
- Search products
- Scan product barcodes
- Add products to the cart
- Modify quantities
- Process payments
- Complete bills
- Generate receipts
- View customer information
- View billing history
- End their shift

---

# 🚀 Key Features

## 🧾 Smart Billing

GreenTill provides a complete supermarket checkout workflow:

```text
Employee Login
      ↓
Start Shift
      ↓
Scan / Search Product
      ↓
Add Product to Cart
      ↓
Enter Quantity
      ↓
Calculate Total
      ↓
Select Payment Method
      ↓
Complete Bill
      ↓
Update Inventory
      ↓
Generate Receipt
