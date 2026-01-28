# -*- coding: utf-8 -*-
{
    'name': "Quản Lý Công Việc",
    'summary': "Module quản lý công việc, task và nhật ký làm việc",
    'description': """
        Module Quản Lý Công Việc
        =========================
        - Quản lý công việc theo dự án
        - Phân loại công việc
        - Theo dõi tiến độ và trạng thái
        - Nhật ký làm việc chi tiết
        - Đánh giá chất lượng công việc
        - Liên kết chặt chẽ với Dự án và Nhân sự
    """,
    'author': "Your Company",
    'website': "http://www.yourcompany.com",
    'category': 'Project Management',
    'version': '1.0',
    'depends': ['base', 'nhan_su', 'quan_ly_du_an', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/loai_cong_viec_view.xml',
        'views/cong_viec_view.xml',
        'views/nhat_ky_cong_viec_view.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}