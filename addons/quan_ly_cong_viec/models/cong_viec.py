from odoo import models, fields, api

class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Quản lý Công việc'
    _rec_name = 'ten_cong_viec'

    ten_cong_viec = fields.Char("Tên công việc", required=True)
    du_an_id = fields.Many2one('du_an', string="Thuộc dự án", required=True, ondelete='cascade')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Người thực hiện", required=True)
    
    ngay_bat_dau = fields.Datetime("Bắt đầu", default=fields.Datetime.now, required=True)
    han_chot = fields.Datetime("Hạn chót", required=True)
    
    chi_phi_du_kien = fields.Float("Chi phí dự kiến")
    phan_tram_tien_do = fields.Integer("Tiến độ (%)", default=0)
    
    muc_do_uu_tien = fields.Selection([
        ('thap', 'Thấp'), ('tb', 'Trung bình'), ('cao', 'Cao')
    ], string="Độ ưu tiên", default='tb')
    
    trang_thai = fields.Selection([
        ('moi', 'Mới giao'), 
        ('dang_lam', 'Đang thực hiện'), 
        ('cho_duyet', 'Chờ duyệt'), 
        ('hoan_thanh', 'Hoàn thành')
    ], string="Trạng thái", default='moi')
    
    ghi_chu = fields.Text("Chi tiết")

    # --- ĐOẠN CODE THÊM MỚI ĐỂ TẠO LOGIC TỰ ĐỘNG ---
    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        if self.trang_thai == 'hoan_thanh':
            self.phan_tram_tien_do = 100
        elif self.trang_thai == 'moi':
            self.phan_tram_tien_do = 0

    @api.onchange('phan_tram_tien_do')
    def _onchange_tien_do(self):
        if self.phan_tram_tien_do == 100:
            self.trang_thai = 'hoan_thanh'
        elif self.phan_tram_tien_do == 0:
            self.trang_thai = 'moi'
        elif 0 < self.phan_tram_tien_do < 100:
            self.trang_thai = 'dang_lam'