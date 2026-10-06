from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from billing_functions import get_bill, get_bill_items
from database import get_connection


# ============================================================
# GREENTILL - RECEIPT GENERATOR
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
RECEIPT_DIR = BASE_DIR / "receipts"

RECEIPT_DIR.mkdir(exist_ok=True)


# ============================================================
# GENERATE RECEIPT
# ============================================================

def generate_receipt(bill_id):

    bill = get_bill(bill_id)

    if bill is None:
        raise ValueError(
            f"Bill '{bill_id}' was not found."
        )

    items = get_bill_items(bill_id)

    if not items:
        raise ValueError(
            f"No items found for bill '{bill_id}'."
        )

    # --------------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------------
    # Customer information is optional. The phone number is
    # intentionally never included on the receipt.
    customer_name = None

    customer_id = bill["customer_id"]

    if customer_id:
        connection = get_connection()

        try:
            customer = connection.execute(
                """
                SELECT name
                FROM customers
                WHERE customer_id = ?
                AND status = 'Active'
                """,
                (customer_id,)
            ).fetchone()

            if customer:
                customer_name = customer["name"]

        finally:
            connection.close()

    receipt_file = RECEIPT_DIR / f"{bill_id}.pdf"

    # --------------------------------------------------------
    # PDF DOCUMENT
    # --------------------------------------------------------

    document = SimpleDocTemplate(
        str(receipt_file),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=35,
        bottomMargin=35
    )

    # --------------------------------------------------------
    # STYLES
    # --------------------------------------------------------

    styles = getSampleStyleSheet()

    store_style = ParagraphStyle(
        "StoreName",
        parent=styles["Heading1"],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=5
    )

    tagline_style = ParagraphStyle(
        "Tagline",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1B5E20"),
        spaceBefore=10,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    right_style = ParagraphStyle(
        "RightText",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT
    )

    total_style = ParagraphStyle(
        "Total",
        parent=styles["Normal"],
        fontSize=15,
        leading=18,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#1B5E20"),
        fontName="Helvetica-Bold"
    )

    eco_style = ParagraphStyle(
        "Eco",
        parent=styles["Normal"],
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1B5E20"),
        fontName="Helvetica-Bold"
    )

    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    story = []

    # Store name
    story.append(
        Paragraph(
            "GreenTill",
            store_style
        )
    )

    story.append(
        Paragraph(
            "Smart Billing. Greener Shopping.",
            tagline_style
        )
    )

    # --------------------------------------------------------
    # BILL INFORMATION
    # --------------------------------------------------------

    bill_info = [
        [
            Paragraph(
                f"<b>Bill ID:</b> {bill['bill_id']}",
                normal_style
            ),
            Paragraph(
                f"<b>Date:</b> {bill['bill_date']}",
                right_style
            )
        ]
    ]

    # Show the customer's full name only when customer details
    # were attached to the bill. Phone number is never printed.
    if customer_name:
        bill_info.append(
            [
                Paragraph(
                    f"<b>Customer:</b> {escape(str(customer_name))}",
                    normal_style
                ),
                Paragraph(
                    "",
                    right_style
                )
            ]
        )

    bill_info.extend(
        [
            [
                Paragraph(
                    f"<b>Employee:</b> {bill['employee_id']}",
                    normal_style
                ),
                Paragraph(
                    f"<b>Time:</b> {bill['bill_time']}",
                    right_style
                )
            ],
            [
                Paragraph(
                    f"<b>Payment:</b> {bill['payment_method']}",
                    normal_style
                ),
                Paragraph(
                    f"<b>Status:</b> {bill['payment_status']}",
                    right_style
                )
            ]
        ]
    )

    bill_info_table = Table(
        bill_info,
        colWidths=[250, 250]
    )

    bill_info_table.setStyle(
        TableStyle([
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    story.append(bill_info_table)

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            "Items",
            heading_style
        )
    )

    # --------------------------------------------------------
    # ITEM TABLE
    # --------------------------------------------------------

    item_data = [
        [
            "Product",
            "Qty",
            "Unit Price",
            "Total"
        ]
    ]

    for item in items:

        quantity_text = (
            f"{item['quantity']:.2f} "
            f"{item['unit']}"
        )

        item_data.append([
            item["product_name"],
            quantity_text,
            f"₹{item['unit_price']:.2f}",
            f"₹{item['item_total']:.2f}"
        ])

    item_table = Table(
        item_data,
        colWidths=[200, 100, 100, 100]
    )

    item_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#E8F5E9")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1B5E20")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#DDDDDD")
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "RIGHT"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(item_table)

    story.append(
        Spacer(1, 15)
    )

    # --------------------------------------------------------
    # BILL SUMMARY
    # --------------------------------------------------------

    summary_data = [
        [
            Paragraph("Subtotal", normal_style),
            Paragraph(
                f"₹{bill['subtotal']:.2f}",
                right_style
            )
        ],
        [
            Paragraph("Discount", normal_style),
            Paragraph(
                f"₹{bill['discount']:.2f}",
                right_style
            )
        ],
        [
            Paragraph("Tax", normal_style),
            Paragraph(
                f"₹{bill['tax']:.2f}",
                right_style
            )
        ],
        [
            Paragraph(
                "<b>GRAND TOTAL</b>",
                normal_style
            ),
            Paragraph(
                f"₹{bill['total_amount']:.2f}",
                total_style
            )
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[350, 150]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "LINEABOVE",
                (0, 3),
                (-1, 3),
                1,
                colors.HexColor("#1B5E20")
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(summary_table)

    story.append(
        Spacer(1, 20)
    )

    # --------------------------------------------------------
    # ECO SCORE
    # --------------------------------------------------------

    eco_data = [
        [
            Paragraph(
                f"🌱 Eco Score: {bill['eco_score']} / 100",
                eco_style
            )
        ]
    ]

    eco_table = Table(
        eco_data,
        colWidths=[500]
    )

    eco_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#E0F2F1")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.HexColor("#B2DFDB")
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                12
            )
        ])
    )

    story.append(eco_table)

    story.append(
        Spacer(1, 25)
    )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Thank you for shopping with GreenTill!",
            ParagraphStyle(
                "Footer",
                parent=styles["Normal"],
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#555555")
            )
        )
    )

    story.append(
        Spacer(1, 5)
    )

    story.append(
        Paragraph(
            "Smart Billing. Greener Shopping.",
            ParagraphStyle(
                "FooterTagline",
                parent=styles["Normal"],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#777777")
            )
        )
    )

    # --------------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------------

    document.build(story)

    return receipt_file


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_bill_id = "B0002"

    try:

        receipt = generate_receipt(
            test_bill_id
        )

        print("=" * 55)
        print("GreenTill Receipt Generator Test")
        print("=" * 55)
        print(f"Bill ID: {test_bill_id}")
        print(f"Receipt created successfully.")
        print(f"Location: {receipt}")
        print("=" * 55)

    except Exception as error:

        print("Receipt generation failed:")
        print(error)