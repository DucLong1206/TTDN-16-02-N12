# -*- coding: utf-8 -*-
{
    'name': "Quản lý Dự án",
    'summary': "Module quản lý dự án (Core)",
    'version': '1.0',
    'author': "Student",
    'depends': ['base', 'nhan_su'],  # KHÔNG CÓ MAIL
    'data': [
        'security/ir.model.access.csv',
        'views/du_an_view.xml',
        'views/menu.xml',
    ],
    'application': True,
}