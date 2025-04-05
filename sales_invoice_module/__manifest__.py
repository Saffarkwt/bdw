{
    "name": "Sales Invoice Module",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": "Custom invoice template for sales invoices",
    "description": """
        This module adds a custom invoice template for sales:
        - Sales invoice template (appears only in customer invoices)
        
        The template is designed to fit on a single page and provides a professional layout.
    """,
    "depends": ["account", "sale"],
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
