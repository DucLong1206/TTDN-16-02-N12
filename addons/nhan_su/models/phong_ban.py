from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin Phòng ban'
    _rec_name='Ten_Phong'
    _order = 'ma_phong'

    ma_phong = fields.Char("Mã Phòng", required=True)
    Ten_Phong = fields.Char("Tên Phòng", required=True)
    Ban_Chuc_Thuoc = fields.Char("Tên phòng ban chực thuộc", required=True)

    
   
   
