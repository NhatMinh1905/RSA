# 🔐 RSA File Transfer App (Python + HTML)

Ứng dụng web đơn giản truyền file có chữ ký số sử dụng thuật toán **RSA**. Người dùng có thể:

✅ Đăng ký / Đăng nhập / Đăng xuất  
✅ Gửi file cho người dùng khác  
✅ Nhận và tải file đã nhận  
✅ Theo dõi lịch sử gửi – nhận file  
## 📁 Cấu trúc thư mục

rsa_file_transfer/
│
├── app.py # Server chính
├── users/ # Lưu thông tin người dùng (file JSON)
├── files/ # Lưu file đã gửi
├── history/ # Lưu lịch sử gửi/nhận (mỗi user 1 file JSON)
│
├── templates/ # Giao diện HTML
│ ├── index.html
│ ├── register.html
│ ├── login.html
│ ├── dashboard.html
│ ├── send_file.html
│ ├── receive_file.html
│ └── history.html
│
├── static/
│ └── style.css # Giao diện CSS cơ bản
│
└── keys/ # (Tùy chọn) Chứa khóa RSA nếu thêm tính năng mã hóa
🧠 Tính năng chính
Tính năng	Mô tả
👤 Đăng ký / Đăng nhập	Lưu thông tin người dùng dưới dạng file JSON
📤 Gửi file	Gửi file đến 1 người dùng khác đã tồn tại
📥 Nhận file	Hiển thị các file gửi đến người dùng hiện tại
🕓 Lịch sử	Hiển thị lịch sử gửi / nhận dưới dạng danh sách
🔐 (Tùy chọn) RSA ký số	Có thể mở rộng để mã hóa/giải mã file bằng RSA
