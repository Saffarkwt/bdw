{
    "name": "Sale Purchase Invoice portal",
    "version": "18.0.0.0",
    "category": "",
    "summary": "",
    "description": """ """,
    "depends": ["account",'sale', 'purchase'],
    "license": 'LGPL-3',
    "data": [
        #"report/invoice_report.xml",
        "report/invoice_report_templates.xml",
        "report/invoice_report_refund.xml",
        "report/product_label_report.xml",
        "views/account_move_view.xml",
        "views/purchase_views.xml",
        "views/partner_views.xml"
    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
