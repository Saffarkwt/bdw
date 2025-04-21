{
    "name": "Receipt Print Module",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Custom receipt printing template for Odoo",
    "description": """
        This module adds a custom receipt printing template that matches the provided design.
        Features:
        - Custom "Display Receipt" template with barcode
        - Company and customer information
        - Product details with serial numbers and model numbers
        - Terms and conditions in both Arabic and English
        - Signature fields
    """,
    "depends": ["account", "sale", "stock"],
    "license": "LGPL-3",
    "data": [
        "views/account_move_view.xml",
        "report/receipt_report.xml",
        "report/receipt_template.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
