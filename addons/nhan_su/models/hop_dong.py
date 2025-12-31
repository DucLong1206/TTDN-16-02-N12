from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Hợp đồng lao động'

    so_hop_dong = fields.Char("Số hợp đồng", required=True)
    
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")

    loai_hop_dong = fields.Selection(
        [
            ('thu_viec', 'Thử việc'),
            ('xac_dinh', 'Xác định thời hạn'),
            ('khong_xac_dinh', 'Không xác định thời hạn')
        ],
        string="Loại hợp đồng",
        required=True
    )

    luong_co_ban = fields.Float("Lương cơ bản")

    trang_thai = fields.Selection(
        [
            ('nhap', 'Nháp'),
            ('hieu_luc', 'Đang hiệu lực'),
            ('het_han', 'Hết hạn')
        ],
        default='nhap',
        string="Trạng thái"
    )

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_ket_thuc < record.ngay_bat_dau:
                raise ValidationError("Ngày kết thúc không được nhỏ hơn ngày bắt đầu")
