# -*- coding: utf-8 -*-
{
    'name': "Quản lý Công việc",
    'summary': "Module Task, Timeline, Kanban",
    'version': '1.0',
    'author': "Student",
    'depends': ['base', 'nhan_su', 'quan_ly_du_an'],
    'data': [
        'security/ir.model.access.csv',
        'views/cong_viec_view.xml',
        'views/du_an_extend_view.xml',  # <--- BẠN ĐANG THIẾU DÒNG NÀY
        'views/menu.xml',
    ],
    'application': True,
}