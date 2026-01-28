# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime

class CongViec(models.Model):
    _name = 'ql.cong_viec'
    _description = 'Quản lý Công việc'
    _rec_name = 'ten_cong_viec'
    _order = 'muc_do_uu_tien desc, han_chot asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_cong_viec = fields.Char(
        string='Mã công việc',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    
    ten_cong_viec = fields.Char(
        string='Tên công việc',
        required=True,
        tracking=True
    )
    
    mo_ta = fields.Text(
        string='Mô tả công việc',
        tracking=True
    )
    
    # ==================== QUAN HỆ VỚI DỰ ÁN ====================
    du_an_id = fields.Many2one(
        'ql.du_an',
        string='Dự án',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    ten_du_an = fields.Char(
        related='du_an_id.ten_du_an',
        string='Tên dự án',
        readonly=True,
        store=True
    )
    
    quan_ly_du_an_id = fields.Many2one(
        related='du_an_id.quan_ly_id',
        string='Quản lý dự án',
        readonly=True,
        store=True
    )
    
    # ==================== PHÂN CÔNG ====================
    nguoi_thuc_hien_id = fields.Many2one(
        'nhan_vien',
        string='Người thực hiện',
        tracking=True
    )
    
    nguoi_giao_viec_id = fields.Many2one(
        'nhan_vien',
        string='Người giao việc',
        default=lambda self: self.env.user.id,
        tracking=True
    )
    
    # ==================== PHÂN LOẠI ====================
    loai_cong_viec_id = fields.Many2one(
        'ql.loai_cong_viec',
        string='Loại công việc',
        tracking=True
    )
    
    # ==================== THỜI GIAN ====================
    ngay_bat_dau = fields.Date(
        string='Ngày bắt đầu',
        default=fields.Date.today
    )
    
    han_chot = fields.Date(
        string='Hạn chót',
        tracking=True
    )
    
    ngay_hoan_thanh = fields.Date(
        string='Ngày hoàn thành thực tế',
        readonly=True
    )
    
    so_ngay_con_lai = fields.Integer(
        string='Số ngày còn lại',
        compute='_compute_so_ngay_con_lai',
        store=True
    )
    
    qua_han = fields.Boolean(
        string='Quá hạn',
        compute='_compute_qua_han',
        store=True
    )
    
    # ==================== ƯU TIÊN & TRẠNG THÁI ====================
    muc_do_uu_tien = fields.Selection([
        ('0', 'Thấp'),
        ('1', 'Trung bình'),
        ('2', 'Cao'),
        ('3', 'Rất cao')
    ],
        string='Mức độ ưu tiên',
        default='1',
        tracking=True
    )
    
    trang_thai = fields.Selection([
        ('todo', 'Cần làm'),
        ('doing', 'Đang làm'),
        ('review', 'Đang đánh giá'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy')
    ],
        string='Trạng thái',
        default='todo',
        required=True,
        tracking=True
    )
    
    # ==================== TIẾN ĐỘ ====================
    tien_do = fields.Integer(
        string='Tiến độ (%)',
        default=0,
        tracking=True
    )
    
    # ==================== NHẬT KÝ LÀM VIỆC ====================
    nhat_ky_ids = fields.One2many(
        'ql.nhat_ky_cong_viec',
        'cong_viec_id',
        string='Nhật ký chi tiết'
    )
    
    tong_gio_lam = fields.Float(
        string='Tổng giờ làm',
        compute='_compute_tong_gio_lam',
        store=True
    )
    
    # ==================== ĐÁNH GIÁ ====================
    diem_danh_gia = fields.Selection([
        ('1', 'Kém'),
        ('2', 'Trung bình'),
        ('3', 'Khá'),
        ('4', 'Tốt'),
        ('5', 'Xuất sắc')
    ],
        string='Đánh giá chất lượng',
        tracking=True
    )
    
    nhan_xet_quan_ly = fields.Text(
        string='Nhận xét của Quản lý',
        tracking=True
    )
    
    # ==================== THÔNG TIN BỔ SUNG ====================
    mau_sac = fields.Integer(
        string='Màu sắc',
        compute='_compute_mau_sac'
    )
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends('han_chot')
    def _compute_so_ngay_con_lai(self):
        today = date.today()
        for record in self:
            if record.han_chot:
                delta = record.han_chot - today
                record.so_ngay_con_lai = delta.days
            else:
                record.so_ngay_con_lai = 0
    
    @api.depends('han_chot', 'trang_thai')
    def _compute_qua_han(self):
        today = date.today()
        for record in self:
            if record.han_chot and record.trang_thai not in ['done', 'cancel']:
                record.qua_han = record.han_chot < today
            else:
                record.qua_han = False
    
    @api.depends('nhat_ky_ids', 'nhat_ky_ids.gio_lam')
    def _compute_tong_gio_lam(self):
        for record in self:
            record.tong_gio_lam = sum(record.nhat_ky_ids.mapped('gio_lam'))
    
    @api.depends('loai_cong_viec_id')
    def _compute_mau_sac(self):
        for record in self:
            if record.loai_cong_viec_id:
                record.mau_sac = record.loai_cong_viec_id.mau_sac
            else:
                record.mau_sac = 0
    
    # ==================== ONCHANGE ====================
    @api.onchange('du_an_id')
    def _onchange_du_an_id(self):
        """Khi chọn dự án, lọc danh sách người thực hiện từ thành viên dự án"""
        if self.du_an_id:
            thanh_vien_ids = self.du_an_id.thanh_vien_ids.filtered(
                lambda x: x.trang_thai == 'active'
            ).mapped('nhan_vien_id')
            return {'domain': {'nguoi_thuc_hien_id': [('id', 'in', thanh_vien_ids.ids)]}}
        return {'domain': {'nguoi_thuc_hien_id': []}}
    
    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        """Tự động cập nhật tiến độ theo trạng thái"""
        if self.trang_thai == 'todo':
            self.tien_do = 0
        elif self.trang_thai == 'doing':
            if self.tien_do == 0:
                self.tien_do = 10
        elif self.trang_thai == 'done':
            self.tien_do = 100
            self.ngay_hoan_thanh = date.today()
    
    # ==================== CONSTRAINTS ====================
    @api.constrains('tien_do')
    def _check_tien_do(self):
        for record in self:
            if record.tien_do < 0 or record.tien_do > 100:
                raise ValidationError('Tiến độ phải từ 0 đến 100%!')
    
    @api.constrains('ngay_bat_dau', 'han_chot')
    def _check_dates(self):
        for record in self:
            if record.han_chot and record.ngay_bat_dau:
                if record.han_chot < record.ngay_bat_dau:
                    raise ValidationError('Hạn chót phải sau ngày bắt đầu!')
    
    @api.constrains('nguoi_thuc_hien_id', 'du_an_id')
    def _check_nguoi_thuc_hien(self):
        """Kiểm tra người thực hiện phải là thành viên của dự án"""
        for record in self:
            if record.nguoi_thuc_hien_id and record.du_an_id:
                thanh_vien = self.env['ql.thanh_vien_du_an'].search([
                    ('du_an_id', '=', record.du_an_id.id),
                    ('nhan_vien_id', '=', record.nguoi_thuc_hien_id.id),
                    ('trang_thai', '=', 'active')
                ])
                if not thanh_vien:
                    raise ValidationError(
                        f'{record.nguoi_thuc_hien_id.ho_va_ten} chưa là thành viên của dự án {record.du_an_id.ten_du_an}!'
                    )
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('ma_cong_viec_unique', 'unique(ma_cong_viec)', 'Mã công việc phải là duy nhất!')
    ]
    
    # ==================== CREATE & WRITE ====================
    @api.model
    def create(self, vals):
        if vals.get('ma_cong_viec', 'New') == 'New':
            vals['ma_cong_viec'] = self.env['ir.sequence'].next_by_code('ql.cong_viec') or 'New'
        return super(CongViec, self).create(vals)
    
    def write(self, vals):
        # Tự động cập nhật ngày hoàn thành khi chuyển sang hoàn thành
        if vals.get('trang_thai') == 'done' and not self.ngay_hoan_thanh:
            vals['ngay_hoan_thanh'] = date.today()
            vals['tien_do'] = 100
        return super(CongViec, self).write(vals)
    
    # ==================== ACTIONS ====================
    def action_start(self):
        """Bắt đầu công việc"""
        self.write({
            'trang_thai': 'doing',
            'ngay_bat_dau': date.today()
        })
    
    def action_complete(self):
        """Hoàn thành công việc"""
        self.write({
            'trang_thai': 'done',
            'tien_do': 100,
            'ngay_hoan_thanh': date.today()
        })
    
    def action_cancel(self):
        """Hủy công việc"""
        self.write({'trang_thai': 'cancel'})
    
    def action_view_worklog(self):
        """Xem nhật ký làm việc"""
        return {
            'name': 'Nhật ký làm việc',
            'type': 'ir.actions.act_window',
            'res_model': 'ql.nhat_ky_cong_viec',
            'view_mode': 'tree,form',
            'domain': [('cong_viec_id', '=', self.id)],
            'context': {
                'default_cong_viec_id': self.id,
                'default_nhan_vien_id': self.nguoi_thuc_hien_id.id
            }
        }