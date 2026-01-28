# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LoaiCongViec(models.Model):
    _name = 'ql.loai_cong_viec'
    _description = 'Loại công việc'
    _rec_name = 'ten_loai'
    _order = 'ten_loai'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ten_loai = fields.Char(
        string='Tên loại công việc',
        required=True
    )
    
    ma_loai = fields.Char(
        string='Mã loại',
        required=True
    )
    
    mo_ta = fields.Text(
        string='Mô tả'
    )
    
    mau_sac = fields.Integer(
        string='Màu sắc',
        help='Màu hiển thị trong kanban'
    )
    
    # ==================== THỐNG KÊ ====================
    so_cong_viec = fields.Integer(
        string='Số công việc',
        compute='_compute_so_cong_viec',
        store=True
    )
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends('ten_loai')
    def _compute_so_cong_viec(self):
        for record in self:
            record.so_cong_viec = self.env['ql.cong_viec'].search_count([
                ('loai_cong_viec_id', '=', record.id)
            ])
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('ma_loai_unique', 'unique(ma_loai)', 'Mã loại công việc phải là duy nhất!')
    ]