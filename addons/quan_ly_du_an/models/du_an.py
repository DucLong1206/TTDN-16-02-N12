# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class DuAn(models.Model):
    _name = 'ql.du_an'
    _description = 'Quản lý Dự án'
    _rec_name = 'ten_du_an'
    _order = 'ngay_bat_dau desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_du_an = fields.Char(
        string='Mã dự án', 
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    
    ten_du_an = fields.Char(
        string='Tên dự án', 
        required=True,
        tracking=True
    )
    
    mo_ta = fields.Text(
        string='Mô tả',
        tracking=True
    )
    
    # ==================== QUẢN LÝ ====================
    quan_ly_id = fields.Many2one(
        'nhan_vien', 
        string='Quản lý dự án',
        required=True,
        tracking=True
    )
    
    # ==================== THỜI GIAN ====================
    ngay_bat_dau = fields.Date(
        string='Ngày bắt đầu',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    
    ngay_ket_thuc = fields.Date(
        string='Ngày kết thúc',
        tracking=True
    )
    
    ngay_ket_thuc_thuc_te = fields.Date(
        string='Ngày kết thúc thực tế',
        readonly=True
    )
    
    so_ngay_thuc_hien = fields.Integer(
        string='Số ngày thực hiện',
        compute='_compute_so_ngay_thuc_hien',
        store=True
    )
    
    # ==================== TRẠNG THÁI & TIẾN ĐỘ ====================
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('planning', 'Lên kế hoạch'),
        ('running', 'Đang thực hiện'),
        ('review', 'Đang đánh giá'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy bỏ')
    ], 
        string='Trạng thái',
        default='draft',
        required=True,
        tracking=True
    )
    
    muc_do_uu_tien = fields.Selection([
        ('0', 'Thấp'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
        ('3', 'Khẩn cấp')
    ], 
        string='Mức độ ưu tiên',
        default='1',
        tracking=True
    )
    
    # ==================== QUAN HỆ VỚI CÁC BẢNG KHÁC ====================
    thanh_vien_ids = fields.One2many(
        'ql.thanh_vien_du_an',
        'du_an_id',
        string='Thành viên dự án'
    )
    
    # ==================== THỐNG KÊ ====================
    so_thanh_vien = fields.Integer(
        string='Số thành viên',
        compute='_compute_so_thanh_vien',
        store=True
    )
    
    # ==================== NGÂN SÁCH ====================
    ngan_sach_du_kien = fields.Float(
        string='Ngân sách dự kiến',
        tracking=True
    )
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_so_ngay_thuc_hien(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc:
                delta = record.ngay_ket_thuc - record.ngay_bat_dau
                record.so_ngay_thuc_hien = delta.days
            else:
                record.so_ngay_thuc_hien = 0
    
    @api.depends('thanh_vien_ids')
    def _compute_so_thanh_vien(self):
        for record in self:
            record.so_thanh_vien = len(record.thanh_vien_ids)
    
    # ==================== CONSTRAINTS ====================
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau:
                if record.ngay_ket_thuc < record.ngay_bat_dau:
                    raise ValidationError('Ngày kết thúc phải sau ngày bắt đầu!')
    
    _sql_constraints = [
        ('ma_du_an_unique', 'unique(ma_du_an)', 'Mã dự án phải là duy nhất!')
    ]
    
    # ==================== CREATE & ACTIONS ====================
    @api.model
    def create(self, vals):
        if vals.get('ma_du_an', 'New') == 'New':
            vals['ma_du_an'] = self.env['ir.sequence'].next_by_code('ql.du_an') or 'New'
        return super(DuAn, self).create(vals)
    
    def action_start_project(self):
        """Bắt đầu dự án"""
        self.write({
            'trang_thai': 'running',
            'ngay_bat_dau': date.today()
        })
    
    def action_complete_project(self):
        """Hoàn thành dự án"""
        self.write({
            'trang_thai': 'done',
            'ngay_ket_thuc_thuc_te': date.today()
        })
    
    def action_cancel_project(self):
        """Hủy dự án"""
        self.write({'trang_thai': 'cancel'})
    
    def action_view_tasks(self):
        """Xem danh sách công việc của dự án"""
        return {
            'name': 'Công việc của dự án',
            'type': 'ir.actions.act_window',
            'res_model': 'ql.cong_viec',
            'view_mode': 'tree,form,kanban',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id}
        }
    
    def action_view_members(self):
        """Xem danh sách thành viên"""
        return {
            'name': 'Thành viên dự án',
            'type': 'ir.actions.act_window',
            'res_model': 'ql.thanh_vien_du_an',
            'view_mode': 'tree,form',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id}
        }