{
    "name": "Custom Invoice Templates",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Custom invoice templates for sales and purchases",
    "description": """
        This module adds separate invoice templates for sales and purchases:
        - Sales invoice template (appears only in customer invoices)
        - Purchase invoice template (appears only in vendor invoices)
        
        Both templates are designed to fit on a single page.
    """,
    "depends": ["account", "sale", "purchase"],
    "license": "LGPL-3",
    "data": [
        "report/invoice_report.xml",
        "report/invoice_templates.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
