# -*- coding: utf-8 -*-
{
    'name': 'Hr Announcement',
    'version': '1.0',
    'summary': 'Hr Announcement',
    'description': """
        Manage Announcement
            Manage Hr Announcement
    """,
    'author': 'Shubh patel',
    'company': 'Acespritech solutions pvt. ltd',
    'website': 'www.acespritech.coms',
    'category': '',
    'depends': ['hr'],
    'data': [
        'security/announcement_security.xml',
        'security/ir.model.access.csv',
        'data/announcement_sequence.xml',
        'views/announcement_announcement_view.xml',
        'views/hr_employee_inherit.xml',
        'report/announcement_report.xml',
        'views/announcement_decalration.xml',
        'data/mail_template.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
