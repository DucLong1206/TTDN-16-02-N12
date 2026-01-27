from odoo import models, fields, api
from datetime import date


class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương nhân viên'
    _order = 'thang desc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True
    )

    thang = fields.Date(
        "Tháng",
        required=True,
    )

    luong_co_ban = fields.Float(
        "Lương cơ bản",
        default=5000000
    )

    so_cong = fields.Integer(
        "Số công",
        compute="_compute_so_cong",
        store=True
    )

    tong_luong = fields.Integer(
        "Tổng lương",
        compute="_compute_luong",
        store=True
    )

    @api.depends('nhan_vien_id', 'thang')
    def _compute_so_cong(self):
        for record in self:
            record.so_cong = 0
            if record.nhan_vien_id and record.thang:
                first_day = record.thang.replace(day=1)
                last_day = record.thang

                cham_cong = self.env['cham_cong'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('ngay', '>=', first_day),
                    ('ngay', '<=', last_day),
                    ('trang_thai', '=', 'di_lam')
                ])
                record.so_cong = len(cham_cong)

    @api.depends('so_cong', 'luong_co_ban')
    def _compute_luong(self):
        SO_CONG_CHUAN = 26
        for record in self:
            record.tong_luong = record.so_cong * (
                record.luong_co_ban / SO_CONG_CHUAN
            )
