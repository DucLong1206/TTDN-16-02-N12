<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    Quản lý dự án + Quản lý công việc
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Platform ERP được áp dụng vào học phần Thực tập doanh nghiệp dựa trên mã nguồn mở Odoo. Dự án này tập trung vào việc xây dựng và tích hợp các module quản lý nhân sự, quản lý dự án và quản lý công việc, nhằm hỗ trợ sinh viên thực hành phát triển hệ thống ERP thực tế. Với nền tảng Odoo, hệ thống cho phép quản lý dữ liệu doanh nghiệp một cách linh hoạt, mở rộng và dễ tùy chỉnh.

---

## 📄 Poster Dự án

<p align="center">
    <a href="./poster.pdf">
        <img src="https://img.shields.io/badge/📄_Xem_Poster_Dự_Án-PDF-red?style=for-the-badge&logo=adobe-acrobat-reader" alt="Poster PDF"/>
    </a>
</p>

> 📌 **Poster** trình bày tổng quan về kiến trúc hệ thống, các phân hệ chính và tính năng nổi bật của dự án. [**Nhấn vào đây để xem Poster (PDF)**](./poster.pdf)

---

## ⚙️ Các phân hệ chính

### 1. Quản lý Nhân sự
- Quản lý thông tin nhân viên, chức vụ, đơn vị công tác
- Theo dõi lịch sử công tác, chứng chỉ, bằng cấp
- Chấm công, tính lương, liên kết với user Odoo

### 2. Quản lý Dự án
- Quản lý dự án từ lập kế hoạch đến hoàn thành, theo dõi thành viên, ngân sách và tiến độ
- Dashboard thống kê với biểu đồ, top nhân viên hiệu quả và cảnh báo dự án sắp hết hạn
- Liên kết chặt chẽ với phân hệ Nhân sự và Công việc

### 3. Quản lý Công việc
- Quản lý nhiệm vụ chi tiết trong dự án, theo dõi trạng thái công việc, nhật ký làm việc
- Đánh giá hiệu suất, assign công việc cho thành viên
- Tích hợp email thông báo và chatter cho thảo luận

---

## 📸 Giao diện & Chức năng

### Dashboard & Thống kê
Dashboard cung cấp cái nhìn tổng quan về dự án và công việc, với thống kê thời gian thực.

| Dashboard Dự án | Top Nhân viên |
|:---:|:---:|
| ![Dashboard Dự án](./docs/screenshots/dashboard_du_an.png) | ![Top Nhân viên](./docs/screenshots/top_nhan_vien.png) |
| *Thống kê tổng quan với card và progress bar* | *Xếp hạng nhân viên hiệu quả nhất* |

| Dự án Gần Hết Hạn | Thống kê Theo Tháng |
|:---:|:---:|
| ![Dự án Gần Hết Hạn](./docs/screenshots/du_an_gan_het_han.png) | ![Thống kê Theo Tháng](./docs/screenshots/thong_ke_theo_thang.png) |
| *Cảnh báo dự án sắp hết hạn* | *Phân tích công việc theo tháng* |

### Phân hệ Quản lý Dự án
Quản lý toàn diện dự án, thành viên và tiến độ.

| Danh sách Dự án | Form Dự án |
|:---:|:---:|
| ![Danh sách Dự án](./docs/screenshots/du_an_tree.png) | ![Form Dự án](./docs/screenshots/du_an_form.png) |
| *Danh sách dự án với trạng thái* | *Chi tiết dự án với notebook thành viên* |

| Kanban Dự án | Thành viên Dự án |
|:---:|:---:|
| ![Kanban Dự án](./docs/screenshots/du_an_kanban.png) | ![Thành viên Dự án](./docs/screenshots/thanh_vien_du_an.png) |
| *View kanban theo trạng thái* | *Quản lý vai trò và thống kê công việc* |

### Phân hệ Nhân sự (HR)
Quản lý hồ sơ nhân sự, quá trình công tác và năng lực nhân viên.

| Hồ sơ Nhân viên | Chấm Công & Lương |
|:---:|:---:|
| ![Nhân sự](./docs/screenshots/nhan_vien_form.png) | ![Chấm Công](./docs/screenshots/cham_cong.png) |
| *Danh sách nhân sự với notebook* | *Quản lý chấm công và bảng lương* |

| Lịch sử Công tác | Chứng chỉ & Bằng cấp |
|:---:|:---:|
| ![Lịch sử Công tác](./docs/screenshots/lich_su_cong_tac.png) | ![Chứng chỉ](./docs/screenshots/danh_sach_chung_chi.png) |
| *Theo dõi quá trình làm việc* | *Quản lý hồ sơ năng lực* |

### Phân hệ Quản lý Công việc
Quản lý nhiệm vụ chi tiết và theo dõi tiến độ.

| Danh sách Công việc | Form Công việc |
|:---:|:---:|
| ![Danh sách Công việc](./docs/screenshots/cong_viec_tree.png) | ![Form Công việc](./docs/screenshots/cong_viec_form.png) |
| *Danh sách công việc với decoration* | *Chi tiết công việc với trạng thái* |

| Nhật ký Công việc | Biểu đồ Ưu tiên |
|:---:|:---:|
| ![Nhật ký Công việc](./docs/screenshots/nhat_ky_cong_viec.png) | ![Biểu đồ Ưu tiên](./docs/screenshots/cong_viec_by_priority.png) |
| *Theo dõi nhật ký làm việc* | *Thống kê công việc theo mức độ ưu tiên* |

---

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🚀 3. Các project đã thực hiện dựa trên Platform

Một số project sinh viên đã thực hiện:
- #### [Khoá 15](./docs/projects/K15/README.md)
- #### [Khoá 16]() (Coming soon)
## ⚙️ 4. Cài đặt

### 4.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 4.1.1. Tải project.
```
git clone https://github.com/FIT-DNU/Business-Internship.git
```
#### 4.1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
#### 4.1.3. Khởi tạo môi trường ảo.
- Khởi tạo môi trường ảo
```
python3.10 -m venv ./venv
```
- Thay đổi trình thông dịch sang môi trường ảo
```
source venv/bin/activate
```
- Chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
pip3 install -r requirements.txt
```
### 4.2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo docker-compose up -d
```
### 4.3. Setup tham số chạy cho hệ thống
Tạo tệp **odoo.conf** có nội dung như sau:
```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```
Có thể kế thừa từ file **odoo.conf.template**
### 4.4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```
Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

## 📝 5. License

© 2024 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---

    
