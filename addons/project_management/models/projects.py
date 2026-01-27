from odoo import models, fields, api
from datetime import date, datetime

class Projects(models.Model):
    _name = 'projects'
    _description = 'Quản lý dự án'

    projects_id = fields.Char("Mã dự án")
    projects_name = fields.Char("Tên dự án")
    
    manager_name = fields.Many2one('nhan_vien', string="Quản lý dự án")

    start_date = fields.Date("Ngày bắt đầu")
    actual_end_date = fields.Date("Ngày kết thúc thực tế")

    progress = fields.Float("Tiến độ (%)", compute='_compute_progress', store=True)
    status = fields.Selection(
        selection=[
            ('not_started', 'Chưa bắt đầu'),
            ('in_progress', 'Đang thực hiện'),
            ('completed', 'Hoàn thành'),
            ('delayed', 'Trì hoãn'),
            ('cancelled', 'Hủy bỏ')
        ], 
        string='Trạng thái', store=True
    )

    ly_do_1 = fields.Text(string="Lý do hủy bỏ", help="Lý do hủy bỏ công việc")

    task_ids = fields.One2many('taskss', inverse_name='projects_id', String='Công việc') 

    @api.depends('task_ids.status')
    def _compute_progress(self):
        for project in self:
            total_tasks = len(project.task_ids)
            completed_tasks = len(project.task_ids.filtered(lambda task: task.status == 'completed'))
            
            if total_tasks > 0:
                project.progress = (completed_tasks / total_tasks) * 100
            else:
                project.progress = 0


    def name_get(self):
        result = []
        for record in self:
            name = f"{record.projects_id}"

            result.append((record.id, name))
        return result
    
    budget_ids = fields.One2many('budgets', inverse_name='projects_id', string="Ngân sách Dự án")

    def action_view_task_chart(self):
        self.ensure_one()  # Đảm bảo phương thức chỉ xử lý một bản ghi
        return {
            'type': 'ir.actions.act_window',
            'name': 'Biểu Đồ Công Việc Công Việc',
            'res_model': 'taskss',
            'view_mode': 'graph',
            'domain': [('projects_id', '=', self.id)],  # Lọc công việc theo dự án hiện tại
            # Đặt giá trị mặc định cho trường projects_id
            'context': {'search_default_group_by_projects_id': self.id},
            'target': 'current',
        }