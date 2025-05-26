{
    "name": "Sr Customization",
    "version": "18.0.0.0",
    "category": "",
    "summary": "Custom Barcode Label Template",
    "description": """
    Custom module for Odoo 18 that provides:
    - Modified barcode label template
    - Custom product methods
    """,
    "author": "Mohamed Abdelrahman",
    "email": "Mohammedeelsayd@gmail.com",
    "website": "https://freelancer-kw.com",
    "mobile": "+96598591476",
    "depends": ["account",'stock', 'purchase', 'product'],
    "license": 'LGPL-3',
    "data": [
        "data/sequence.xml",
        "views/account_move.xml",
        "views/purchase_view.xml",
        "report/product_label_report.xml"
    ],
    "images": [
        "static/description/icon.png"
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
