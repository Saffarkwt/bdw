{
    'name': 'Purchase Invoice Standalone',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Standalone Purchase Invoice Template',
    'description': """
        This module provides a standalone purchase invoice template 
        that is completely separate from other invoice templates.
        
        Features:
        - Custom purchase invoice template without unit price column
        - Updated terms and conditions for purchase invoices
        - Direct print button for purchase invoices
    """,
    'author': 'Blue Diamond',
    'depends': ['account'],
    'data': [
        'views/account_move_view.xml',
        'report/purchase_invoice_report.xml',
        'report/purchase_invoice_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
