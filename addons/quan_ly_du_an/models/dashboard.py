# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta

class DashboardDuAn(models.TransientModel):
    _name = 'ql.dashboard.du_an'
    _description = 'Dashboard Quản lý Dự án'

    # ==================== THỐNG KÊ TỔNG QUAN ====================
    tong_so_du_an = fields.Integer(
        string='Tổng số dự án',
        compute='_compute_thong_ke_tong_quan'
    )
    
    tong_so_cong_viec = fields.Integer(
        string='Tổng số công việc',
        compute='_compute_thong_ke_tong_quan'
    )
    
    du_an_dang_thuc_hien = fields.Integer(
        string='Dự án đang thực hiện',
        compute='_compute_thong_ke_tong_quan'
    )
    
    du_an_hoan_thanh = fields.Integer(
        string='Dự án hoàn thành',
        compute='_compute_thong_ke_tong_quan'
    )
    
    cong_viec_dang_lam = fields.Integer(
        string='Công việc đang làm',
        compute='_compute_thong_ke_tong_quan'
    )
    
    cong_viec_hoan_thanh = fields.Integer(
        string='Công việc hoàn thành',
        compute='_compute_thong_ke_tong_quan'
    )
    
    cong_viec_qua_han = fields.Integer(
        string='Công việc quá hạn',
        compute='_compute_thong_ke_tong_quan'
    )
    
    ty_le_hoan_thanh_du_an = fields.Float(
        string='Tỷ lệ hoàn thành dự án (%)',
        compute='_compute_thong_ke_tong_quan'
    )
    
    ty_le_hoan_thanh_cong_viec = fields.Float(
        string='Tỷ lệ hoàn thành công việc (%)',
        compute='_compute_thong_ke_tong_quan'
    )
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends()
    def _compute_thong_ke_tong_quan(self):
        for record in self:
            # Thống kê dự án
            du_an_obj = self.env['ql.du_an']
            record.tong_so_du_an = du_an_obj.search_count([])
            record.du_an_dang_thuc_hien = du_an_obj.search_count([('trang_thai', '=', 'running')])
            record.du_an_hoan_thanh = du_an_obj.search_count([('trang_thai', '=', 'done')])
            
            # Tỷ lệ hoàn thành dự án
            if record.tong_so_du_an > 0:
                record.ty_le_hoan_thanh_du_an = (record.du_an_hoan_thanh / record.tong_so_du_an) * 100
            else:
                record.ty_le_hoan_thanh_du_an = 0
            
            # Thống kê công việc
            cong_viec_obj = self.env['ql.cong_viec']
            record.tong_so_cong_viec = cong_viec_obj.search_count([])
            record.cong_viec_dang_lam = cong_viec_obj.search_count([('trang_thai', 'in', ['doing', 'review'])])
            record.cong_viec_hoan_thanh = cong_viec_obj.search_count([('trang_thai', '=', 'done')])
            record.cong_viec_qua_han = cong_viec_obj.search_count([('qua_han', '=', True)])
            
            # Tỷ lệ hoàn thành công việc
            if record.tong_so_cong_viec > 0:
                record.ty_le_hoan_thanh_cong_viec = (record.cong_viec_hoan_thanh / record.tong_so_cong_viec) * 100
            else:
                record.ty_le_hoan_thanh_cong_viec = 0
    
    # ==================== ACTIONS ====================
    def action_view_du_an_running(self):
        """Xem dự án đang thực hiện"""
        return {
            'name': 'Dự án đang thực hiện',
            'type': 'ir.actions.act_window',
            'res_model': 'ql.du_an',
            'view_mode': 'kanban,tree,form',
            'domain': [('trang_thai', '=', 'running')],
        }
    
    def action_view_cong_viec_overdue(self):
        """Xem công việc quá hạn"""
        return {
            'name': 'Công việc quá hạn',
            'type': 'ir.actions.act_window',
            'res_model': 'ql.cong_viec',
            'view_mode': 'tree,form,kanban',
            'domain': [('qua_han', '=', True)],
        }
    
    def get_du_an_by_status(self):
        """Lấy dữ liệu dự án theo trạng thái cho biểu đồ"""
        du_an_obj = self.env['ql.du_an']
        
        data = []
        statuses = [
            ('draft', 'Nháp'),
            ('planning', 'Lên kế hoạch'),
            ('running', 'Đang thực hiện'),
            ('review', 'Đang đánh giá'),
            ('done', 'Hoàn thành'),
            ('cancel', 'Hủy bỏ')
        ]
        
        for status, label in statuses:
            count = du_an_obj.search_count([('trang_thai', '=', status)])
            if count > 0:
                data.append({
                    'label': label,
                    'value': count,
                    'status': status
                })
        
        return data
    
    def get_top_nhan_vien(self, limit=5):
        """Lấy top nhân viên hiệu quả nhất"""
        query = """
            SELECT 
                nv.id,
                nv.ho_va_ten,
                COUNT(DISTINCT cv.id) as so_cong_viec,
                COUNT(DISTINCT CASE WHEN cv.trang_thai = 'done' THEN cv.id END) as so_cv_hoan_thanh,
                ROUND(
                    CAST(COUNT(DISTINCT CASE WHEN cv.trang_thai = 'done' THEN cv.id END) AS NUMERIC) * 100.0 / 
                    NULLIF(COUNT(DISTINCT cv.id), 0), 
                    2
                ) as ty_le_hoan_thanh,
                SUM(COALESCE(nk.gio_lam, 0)) as tong_gio_lam
            FROM nhan_vien nv
            LEFT JOIN ql_cong_viec cv ON cv.nguoi_thuc_hien_id = nv.id
            LEFT JOIN ql_nhat_ky_cong_viec nk ON nk.nhan_vien_id = nv.id
            WHERE cv.id IS NOT NULL
            GROUP BY nv.id, nv.ho_va_ten
            HAVING COUNT(DISTINCT cv.id) > 0
            ORDER BY ty_le_hoan_thanh DESC, so_cv_hoan_thanh DESC
            LIMIT %s
        """
        
        self.env.cr.execute(query, (limit,))
        results = self.env.cr.dictfetchall()
        
        return results
    
    def get_cong_viec_by_priority(self):
        """Lấy dữ liệu công việc theo mức độ ưu tiên"""
        cong_viec_obj = self.env['ql.cong_viec']
        
        priorities = [
            ('0', 'Thấp'),
            ('1', 'Trung bình'),
            ('2', 'Cao'),
            ('3', 'Rất cao')
        ]
        
        data = []
        for priority, label in priorities:
            count = cong_viec_obj.search_count([('muc_do_uu_tien', '=', priority)])
            if count > 0:
                data.append({
                    'label': label,
                    'value': count,
                    'priority': priority
                })
        
        return data
    
    def get_du_an_gan_het_han(self, days=7):
        """Lấy dự án sắp hết hạn"""
        today = date.today()
        deadline = today + timedelta(days=days)
        
        du_an_obj = self.env['ql.du_an']
        du_ans = du_an_obj.search([
            ('ngay_ket_thuc', '>=', today),
            ('ngay_ket_thuc', '<=', deadline),
            ('trang_thai', 'in', ['running', 'review'])
        ], order='ngay_ket_thuc asc')
        
        result = []
        for du_an in du_ans:
            days_left = (du_an.ngay_ket_thuc - today).days
            result.append({
                'id': du_an.id,
                'ten': du_an.ten_du_an,
                'ngay_ket_thuc': du_an.ngay_ket_thuc,
                'so_ngay_con_lai': days_left,
                'quan_ly': du_an.quan_ly_id.ho_va_ten if du_an.quan_ly_id else '',
            })
        
        return result
    
    def get_thong_ke_theo_thang(self, months=6):
        """Lấy thống kê công việc theo tháng"""
        query = """
            SELECT 
                TO_CHAR(ngay_bat_dau, 'YYYY-MM') as thang,
                COUNT(*) as tong_cong_viec,
                COUNT(CASE WHEN trang_thai = 'done' THEN 1 END) as da_hoan_thanh,
                COUNT(CASE WHEN trang_thai IN ('doing', 'review') THEN 1 END) as dang_lam,
                COUNT(CASE WHEN qua_han = true THEN 1 END) as qua_han
            FROM ql_cong_viec
            WHERE ngay_bat_dau >= CURRENT_DATE - INTERVAL '%s months'
            GROUP BY thang
            ORDER BY thang DESC
        """
        
        self.env.cr.execute(query, (months,))
        results = self.env.cr.dictfetchall()
        
        return results