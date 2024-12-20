# -*- coding: utf-8 -*-
{
    'name': 'Hr Management System',
    'version': '1.0',
    'summary': 'Hr Management System',
    'description': """
        Manage Hr System
            Manage Hr Help Desk
    """,
    'author': 'Shubh patel',
    'company': 'Acespritech solutions pvt. ltd',
    'website': 'www.acespritech.coms',
    'category': '',
    'depends': ['hr_announcement', 'hr_holidays', 'hr_attendance', 'hr_timesheet', 'web_unsplash'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_management_security.xml',
        'views/hr_management_menu_views.xml',
        'views/employee_timesheet_view.xml',
        'data/mail_template.xml',
        'data/birthday_cron.xml',
        'data/birthday_mail_template.xml',
        'views/hr_employee_view.xml',
        'views/hr_leave_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
