from datetime import date
from odoo import models, fields, api

class Taskss(models.Model):
    _name = 'taskss'
    _description = 'Quản lý công việc'

    taskss_id = fields.Char('Mã công việc')
    taskss_name = fields.Char('Tên công việc',required=True)
    projects_id = fields.Many2one('projects', string='Dự án')

    nhan_vien_ids = fields.Many2many('nhan_vien', string='Thành viên tham gia', help='Chọn các thành viên tham gia dự án')
    expense_ids = fields.One2many('expenses', inverse_name='taskss_id', string="Chi phí Dự án")

    start_date = fields.Date('Ngày bắt đầu')
    deadline = fields.Date('Hạn Chót')

    priority = fields.Selection(
        selection=[
            ('low', 'Thấp'),
            ('medium', 'Trung bình'),
            ('high', 'Cao'),
        ],
    string = 'Mức độ ưu tiên'
    )

    progress = fields.Float('Tiến Độ (%)', compute='_compute_progress', store=True)

    status = fields.Selection(
        selection=[
            ('not_started', 'Chưa bắt đầu'),
            ('in_progress', 'Đang thực hiện'),
            ('completed', 'Hoàn thành'),
            ('delayed', 'Trì hoãn'),
            ('cancelled', 'Hủy bỏ')
        ], 
        string='Trạng thái'
    )
    ly_do = fields.Text(string="Lý do hủy bỏ", help="Lý do hủy bỏ công việc")

    @api.depends('start_date', 'deadline')
    def _compute_progress(self):
        today = date.today()
        for project in self:
            if project.start_date and project.deadline:
                total_days = (project.deadline - project.start_date).days
                elapsed_days = (today - project.start_date).days

                if total_days > 0:
                    project.progress = max(0, min(100, (elapsed_days / total_days) * 100))
                else:
                    project.progress = 100 if today >= project.deadline else 0
            else:
                project.progress = 0

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.taskss_name}" 
            result.append((record.id, name))
        return result
    