{
    'name': 'Expenses Custom',
    'version': '17.0.0.1.0',
    'author': 'Mohsen Mohamed',
    'depends': ['hr_expense'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/report_view_inherit.xml',
        'views/expense_view_inherit.xml',
        'views/expense_category_view.xml',
        'wizard/reject_wizard_view.xml',
        'wizard/recall_wizard_view.xml',
    ],
}
