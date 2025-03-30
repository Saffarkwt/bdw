{
    'name': 'Employee End of Service',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage employee end of service according to Kuwaiti labor law',
    'description': """
        This module allows you to manage employee end of service calculations and settlements
        according to Kuwaiti labor law. It includes:
        
        * End of service reasons configuration
        * End of service calculation formulas based on reason
        * End of service request workflow with approvals
        * End of service settlement calculations
        * Integration with HR contracts and leave management
    """,
    'author': 'Manus',
    'website': '',
    'depends': [
        'hr',
        'hr_contract',
        'hr_holidays',
        'account',
    ],
    'data': [
        # Load security groups first
        'security/eos_security.xml',
        'security/ir.model.access.csv',
        
        # Load data
        'data/eos_data.xml',
        
        # Load wizards before views that reference them
        'wizards/eos_calculation_views.xml',
        
        # Load views
        'views/eos_settings_views.xml',
        'views/eos_reason_views.xml',
        'views/eos_request_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/menu_views.xml',
        
        # Load reports
        'report/eos_report_actions.xml',
        'report/eos_report_templates.xml',
        
        # Load multi-company rules last
        'security/eos_multi_company_rules.xml',
    ],
    'demo': [
        'demo/eos_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
