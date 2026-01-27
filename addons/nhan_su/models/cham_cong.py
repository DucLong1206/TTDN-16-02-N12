from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Bảng chấm công'
    _order = 'ngay desc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    ngay = fields.Date(
        string="Ngày chấm công",
        required=True
    )

    gio_vao = fields.Integer("Giờ vào")
    gio_ra = fields.Integer("Giờ ra")

    so_gio_lam = fields.Integer(
        "Số giờ làm",
        compute="_compute_so_gio_lam",
        store=True
    )

    trang_thai = fields.Selection(
        [
            ('di_lam', 'Đi làm'),
            ('nghi', 'Nghỉ'),
            ('nghi_phep', 'Nghỉ phép')
        ],
        string="Trạng thái",
        default='di_lam'
    )

    @api.depends('gio_vao', 'gio_ra')
    def _compute_so_gio_lam(self):
        for record in self:
            if record.gio_vao and record.gio_ra and record.gio_ra > record.gio_vao:
                record.so_gio_lam = record.gio_ra - record.gio_vao
            else:
                record.so_gio_lam = 0

    @api.constrains('gio_vao', 'gio_ra')
    def _check_gio(self):
        for record in self:
            if record.gio_vao and record.gio_ra and record.gio_ra < record.gio_vao:
                raise ValidationError("Giờ ra phải lớn hơn giờ vào")
