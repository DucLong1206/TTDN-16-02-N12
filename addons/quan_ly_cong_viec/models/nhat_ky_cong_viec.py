# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NhatKyCongViec(models.Model):
    _name = 'ql.nhat_ky_cong_viec'
    _description = 'Nhật ký công việc'
    _rec_name = 'cong_viec_id'
    _order = 'ngay_thuc_hien desc, id desc'

    # ==================== QUAN HỆ ====================
    cong_viec_id = fields.Many2one(
        'ql.cong_viec',
        string='Công việc',
        required=True,
        ondelete='cascade'
    )
    
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True,
        ondelete='restrict'
    )
    
    # ==================== THÔNG TIN TỪ CÔNG VIỆC ====================
    du_an_id = fields.Many2one(
        related='cong_viec_id.du_an_id',
        string='Dự án',
        readonly=True,
        store=True
    )
    
    ten_cong_viec = fields.Char(
        related='cong_viec_id.ten_cong_viec',
        string='Tên công việc',
        readonly=True,
        store=True
    )
    
    # ==================== THỜI GIAN ====================
    ngay_thuc_hien = fields.Date(
        string='Ngày thực hiện',
        default=fields.Date.today,
        required=True
    )
    
    gio_bat_dau = fields.Float(
        string='Giờ bắt đầu',
        help='Ví dụ: 8.5 = 8:30'
    )
    
    gio_ket_thuc = fields.Float(
        string='Giờ kết thúc',
        help='Ví dụ: 17.5 = 17:30'
    )
    
    gio_lam = fields.Float(
        string='Số giờ làm',
        required=True,
        default=1.0
    )
    
    # ==================== NỘI DUNG ====================
    mo_ta_chi_tiet = fields.Text(
        string='Nội dung công việc đã thực hiện',
        required=True
    )
    
    ket_qua = fields.Text(
        string='Kết quả đạt được'
    )
    
    kho_khan = fields.Text(
        string='Khó khăn gặp phải'
    )
    
    # ==================== TIẾN ĐỘ ====================
    tien_do_cap_nhat = fields.Integer(
        string='Tiến độ cập nhật (%)',
        help='Tiến độ của công việc sau khi làm việc này'
    )
    
    # ==================== FILE ĐÍNH KÈM ====================
    file_dinh_kem_ids = fields.Many2many(
        'ir.attachment',
        string='File đính kèm'
    )
    
    # ==================== GHI CHÚ ====================
    ghi_chu = fields.Text(
        string='Ghi chú'
    )
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends('gio_bat_dau', 'gio_ket_thuc')
    def _compute_gio_lam_auto(self):
        for record in self:
            if record.gio_bat_dau and record.gio_ket_thuc:
                record.gio_lam = record.gio_ket_thuc - record.gio_bat_dau
    
    # ==================== CONSTRAINTS ====================
    @api.constrains('gio_lam')
    def _check_gio_lam(self):
        for record in self:
            if record.gio_lam <= 0:
                raise ValidationError('Số giờ làm phải lớn hơn 0!')
            if record.gio_lam > 24:
                raise ValidationError('Số giờ làm không được vượt quá 24 giờ!')
    
    @api.constrains('gio_bat_dau', 'gio_ket_thuc')
    def _check_gio(self):
        for record in self:
            if record.gio_bat_dau and record.gio_ket_thuc:
                if record.gio_ket_thuc <= record.gio_bat_dau:
                    raise ValidationError('Giờ kết thúc phải sau giờ bắt đầu!')
    
    @api.constrains('tien_do_cap_nhat')
    def _check_tien_do(self):
        for record in self:
            if record.tien_do_cap_nhat:
                if record.tien_do_cap_nhat < 0 or record.tien_do_cap_nhat > 100:
                    raise ValidationError('Tiến độ phải từ 0 đến 100%!')
    
    # ==================== ONCHANGE ====================
    @api.onchange('cong_viec_id')
    def _onchange_cong_viec_id(self):
        """Tự động điền người thực hiện từ công việc"""
        if self.cong_viec_id and self.cong_viec_id.nguoi_thuc_hien_id:
            self.nhan_vien_id = self.cong_viec_id.nguoi_thuc_hien_id
            self.tien_do_cap_nhat = self.cong_viec_id.tien_do
    
    @api.onchange('gio_bat_dau', 'gio_ket_thuc')
    def _onchange_gio(self):
        """Tự động tính số giờ làm"""
        if self.gio_bat_dau and self.gio_ket_thuc and self.gio_ket_thuc > self.gio_bat_dau:
            self.gio_lam = self.gio_ket_thuc - self.gio_bat_dau
    
    # ==================== CREATE & WRITE ====================
    @api.model
    def create(self, vals):
        result = super(NhatKyCongViec, self).create(vals)
        # Cập nhật tiến độ công việc nếu có
        if result.tien_do_cap_nhat and result.cong_viec_id:
            result.cong_viec_id.write({'tien_do': result.tien_do_cap_nhat})
        return result
    
    def write(self, vals):
        result = super(NhatKyCongViec, self).write(vals)
        # Cập nhật tiến độ công việc nếu có thay đổi
        if 'tien_do_cap_nhat' in vals:
            for record in self:
                if record.tien_do_cap_nhat and record.cong_viec_id:
                    record.cong_viec_id.write({'tien_do': record.tien_do_cap_nhat})
        return result