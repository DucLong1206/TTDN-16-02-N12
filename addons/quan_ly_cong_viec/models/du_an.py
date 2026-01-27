from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Dự Án'
    _rec_name = 'ten_du_an'

    ten_du_an = fields.Char(string='Tên Dự Án', required=True)
    mo_ta = fields.Text(string='Mô Tả')
    # tien_do_du_an = fields.Float(string="Tiến Độ Dự Án (%)", compute="_compute_tien_do", store=True)
    
    nguoi_phu_trach_id = fields.Many2one('nhan_vien', string='Người Phụ Trách', ondelete='set null')

    nhan_vien_ids = fields.Many2many('nhan_vien', 'du_an_nhan_vien_rel', 'du_an_id', 'nhan_vien_id', string='Nhân Viên Tham Gia')

    tai_nguyen_ids = fields.One2many('tai_nguyen', 'du_an_id', string='Danh Sách Tài Nguyên')

    cong_viec_ids = fields.One2many('cong_viec', 'du_an_id', string='Công Việc')
        
    dashboard_id = fields.Many2one('dashboard', string="Dashboard")

    
    danh_gia_nhan_vien_ids = fields.One2many('danh_gia_nhan_vien', 'du_an_id', string='Đánh Giá Nhân Viên')
    tien_do_du_an = fields.Selection([
        ('chua_bat_dau', 'Chưa Bắt Đầu'),
        ('dang_thuc_hien', 'Đang Thực Hiện'),
        ('hoan_thanh', 'Hoàn Thành'),
        ('tam_dung', 'Tạm Dừng')
    ], string="Trạng Thái Dự Án", default='chua_bat_dau')
    phan_tram_du_an = fields.Float(string="Tiến Độ Dự Án (%)", default=0.0)
    nhat_ky_cong_viec_ids = fields.One2many('nhat_ky_cong_viec', 'du_an_id', string='Nhật Ký Công Việc')

    @api.depends('tien_do_du_an')
    def _compute_phan_tram(self):
        """ Cập nhật phần trăm hoàn thành theo trạng thái dự án """
        for record in self:
            if record.tien_do_du_an == 'chua_bat_dau':
                record.phan_tram_du_an = 0.0  # Nếu "Chưa Bắt Đầu", phần trăm luôn là 0.
    
    @api.constrains('phan_tram_du_an', 'tien_do_du_an')
    def _check_phan_tram_du_an(self):
        """ Kiểm tra điều kiện hợp lệ cho phần trăm hoàn thành """
        for record in self:
            if record.tien_do_du_an == 'chua_bat_dau' and record.phan_tram_du_an != 0:
                raise ValidationError("Tiến độ dự án phải là 0% khi dự án ở trạng thái 'Chưa Bắt Đầu'.")
            if record.phan_tram_du_an < 0 or record.phan_tram_du_an > 100:
                raise ValidationError("Tiến độ dự án phải nằm trong khoảng từ 0% đến 100%.")
            
    @api.model
    def create(self, vals):
        """ Đảm bảo người phụ trách có trong danh sách nhân viên tham gia khi tạo dự án """
        nguoi_phu_trach_id = vals.get('nguoi_phu_trach_id')
        nhan_vien_ids = vals.get('nhan_vien_ids', [(6, 0, [])])  # Mặc định là danh sách rỗng nếu không có

        if nguoi_phu_trach_id:
            # Lấy danh sách nhân viên hiện có
            nhan_vien_list = set(nhan_vien_ids[0][2]) if nhan_vien_ids else set()
            # Thêm người phụ trách vào danh sách
            nhan_vien_list.add(nguoi_phu_trach_id)
            vals['nhan_vien_ids'] = [(6, 0, list(nhan_vien_list))]

        return super(DuAn, self).create(vals)

    def write(self, vals):
        """ Đảm bảo người phụ trách có trong danh sách nhân viên tham gia khi cập nhật dự án """
        for record in self:
            nguoi_phu_trach_id = vals.get('nguoi_phu_trach_id', record.nguoi_phu_trach_id.id)
            nhan_vien_ids = vals.get('nhan_vien_ids', [(6, 0, record.nhan_vien_ids.ids)])

            if nguoi_phu_trach_id:
                nhan_vien_list = set(nhan_vien_ids[0][2]) if nhan_vien_ids else set()
                nhan_vien_list.add(nguoi_phu_trach_id)
                vals['nhan_vien_ids'] = [(6, 0, list(nhan_vien_list))]

        return super(DuAn, self).write(vals)
    
    @api.depends('cong_viec_ids.phan_tram_cong_viec')
    def _compute_phan_tram_du_an(self):
        for record in self:
            if record.cong_viec_ids:
                total_progress = sum(record.cong_viec_ids.mapped('phan_tram_cong_viec'))
                record.phan_tram_du_an = total_progress / len(record.cong_viec_ids)
            else:
                record.phan_tram_du_an = 0.0
