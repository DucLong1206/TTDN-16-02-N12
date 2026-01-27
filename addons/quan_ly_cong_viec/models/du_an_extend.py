from odoo import models, fields, api

class DuAnExtend(models.Model):
    _inherit = 'du_an'  # Kế thừa module dự án

    # Thêm các field này vào dự án từ phía công việc
    cong_viec_ids = fields.One2many('cong_viec', 'du_an_id', string="Danh sách công việc")
    
    tong_chi_phi = fields.Float("Tổng chi phí", compute="_compute_tong_hop", store=True)
    tien_do_du_an = fields.Float("Tiến độ tổng thể (%)", compute="_compute_tong_hop", store=True)

    @api.depends('cong_viec_ids.chi_phi_du_kien', 'cong_viec_ids.phan_tram_tien_do')
    def _compute_tong_hop(self):
        for rec in self:
            rec.tong_chi_phi = sum(line.chi_phi_du_kien for line in rec.cong_viec_ids)
            if len(rec.cong_viec_ids) > 0:
                rec.tien_do_du_an = sum(line.phan_tram_tien_do for line in rec.cong_viec_ids) / len(rec.cong_viec_ids)
            else:
                rec.tien_do_du_an = 0.0