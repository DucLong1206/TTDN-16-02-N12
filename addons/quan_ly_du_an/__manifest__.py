# -*- coding: utf-8 -*-
{
    'name': "Quản Lý Dự Án",
    'summary': "Module quản lý dự án, thành viên và tiến độ",
    'description': """
        Module Quản Lý Dự Án
        ====================
        - Quản lý thông tin dự án
        - Quản lý thành viên tham gia dự án
        - Theo dõi tiến độ và trạng thái dự án
        - Liên kết với module Nhân sự và Công việc
    """,
    'author': "Your Company",
    'website': "http://www.yourcompany.com",
    'category': 'Project Management',
    'version': '1.0',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/du_an_view.xml',
        'views/thanh_vien_du_an_view.xml',
        'views/dashboard_view.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}