from odoo import models, fields

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Quản lý Dự án'
    _rec_name = 'ten_du_an'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ma_du_an = fields.Char("Mã dự án", required=True)
    ten_du_an = fields.Char("Tên dự án", required=True)
    quan_ly_id = fields.Many2one('nhan_vien', string="Trưởng dự án", required=True)
    
    ngay_bat_dau = fields.Date("Ngày bắt đầu")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    trang_thai = fields.Selection([
        ('khoi_tao', 'Khởi tạo'),
        ('dang_chay', 'Đang chạy'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành')
    ], string="Trạng thái", default='khoi_tao')
    
    mo_ta = fields.Text("Mô tả dự án")
    
  