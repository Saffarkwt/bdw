{
    'name': 'Stock Picking Display Receipt',
    'version': '1.0',
    'summary': 'Custom Display Receipt for stock.picking',
    'category': 'Stock',
    'author': 'YourCompany',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'report/display_receipt_template.xml',
        'report/report_action.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
