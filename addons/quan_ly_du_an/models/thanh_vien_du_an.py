# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ThanhVienDuAn(models.Model):
    _name = 'ql.thanh_vien_du_an'
    _description = 'Thành viên tham gia dự án'
    _rec_name = 'nhan_vien_id'
    _order = 'vai_tro, ngay_tham_gia desc'

    # ==================== QUAN HỆ ====================
    du_an_id = fields.Many2one(
        'ql.du_an',
        string='Dự án',
        required=True,
        ondelete='cascade'
    )
    
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True,
        ondelete='restrict'
    )
    
    # ==================== THÔNG TIN VAI TRÒ ====================
    vai_tro = fields.Selection([
        ('leader', 'Trưởng nhóm'),
        ('member', 'Thành viên'),
        ('supporter', 'Hỗ trợ'),
        ('reviewer', 'Đánh giá')
    ],
        string='Vai trò',
        required=True,
        default='member'
    )
    
    # ==================== THỜI GIAN ====================
    ngay_tham_gia = fields.Date(
        string='Ngày tham gia',
        default=fields.Date.today,
        required=True
    )
    
    ngay_ket_thuc = fields.Date(
        string='Ngày kết thúc'
    )
    
    trang_thai = fields.Selection([
        ('active', 'Đang hoạt động'),
        ('inactive', 'Ngừng hoạt động')
    ],
        string='Trạng thái',
        default='active'
    )
    
    # ==================== THÔNG TIN BỔ SUNG ====================
    mo_ta_nhiem_vu = fields.Text(
        string='Mô tả nhiệm vụ'
    )
    
    phan_tram_tham_gia = fields.Float(
        string='% Tham gia',
        default=100.0,
        help='Phần trăm thời gian tham gia dự án'
    )
    
    # ==================== THỐNG KÊ ====================
    so_cong_viec_duoc_giao = fields.Integer(
        string='Số công việc được giao',
        compute='_compute_thong_ke_cong_viec',
        store=True
    )
    
    so_cong_viec_hoan_thanh = fields.Integer(
        string='Số công việc hoàn thành',
        compute='_compute_thong_ke_cong_viec',
        store=True
    )
    
    ty_le_hoan_thanh = fields.Float(
        string='Tỷ lệ hoàn thành (%)',
        compute='_compute_thong_ke_cong_viec',
        store=True
    )
    
    # ==================== THÔNG TIN TỪ NHÂN VIÊN ====================
    email = fields.Char(
        related='nhan_vien_id.email',
        string='Email',
        readonly=True
    )
    
    so_dien_thoai = fields.Char(
        related='nhan_vien_id.so_dien_thoai',
        string='Số điện thoại',
        readonly=True
    )
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends('nhan_vien_id', 'du_an_id')
    def _compute_thong_ke_cong_viec(self):
        for record in self:
            cong_viecs = self.env['ql.cong_viec'].search([
                ('du_an_id', '=', record.du_an_id.id),
                ('nguoi_thuc_hien_id', '=', record.nhan_vien_id.id)
            ])
            
            record.so_cong_viec_duoc_giao = len(cong_viecs)
            record.so_cong_viec_hoan_thanh = len(cong_viecs.filtered(lambda x: x.trang_thai == 'done'))
            
            if record.so_cong_viec_duoc_giao > 0:
                record.ty_le_hoan_thanh = (record.so_cong_viec_hoan_thanh / record.so_cong_viec_duoc_giao) * 100
            else:
                record.ty_le_hoan_thanh = 0
    
    # ==================== CONSTRAINTS ====================
    @api.constrains('nhan_vien_id', 'du_an_id')
    def _check_unique_member(self):
        for record in self:
            existing = self.search([
                ('du_an_id', '=', record.du_an_id.id),
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('id', '!=', record.id),
                ('trang_thai', '=', 'active')
            ])
            if existing:
                raise ValidationError('Nhân viên này đã tham gia dự án!')
    
    @api.constrains('phan_tram_tham_gia')
    def _check_phan_tram(self):
        for record in self:
            if record.phan_tram_tham_gia < 0 or record.phan_tram_tham_gia > 100:
                raise ValidationError('Phần trăm tham gia phải từ 0 đến 100!')
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('unique_member_project', 
         'unique(du_an_id, nhan_vien_id)', 
         'Nhân viên không thể tham gia dự án nhiều lần!')
    ]
    
    # ==================== ACTIONS ====================
    def action_view_tasks(self):
        """Xem công việc của thành viên trong dự án"""
        return {
            'name': 'Công việc của ' + self.nhan_vien_id.ho_va_ten,
            'type': 'ir.actions.act_window',
            'res_model': 'ql.cong_viec',
            'view_mode': 'tree,form,kanban',
            'domain': [
                ('du_an_id', '=', self.du_an_id.id),
                ('nguoi_thuc_hien_id', '=', self.nhan_vien_id.id)
            ]
        }
    
    def action_deactivate(self):
        """Ngừng hoạt động"""
        self.write({
            'trang_thai': 'inactive',
            'ngay_ket_thuc': fields.Date.today()
        })