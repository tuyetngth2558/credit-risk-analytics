# 🚀 Deploy Dashboard Lên Streamlit Cloud - Hướng Dẫn Chi Tiết

## ✨ Kết quả: Dashboard tương tác ONLINE miễn phí

Sau khi làm theo hướng dẫn này, bạn sẽ có:
- ✅ Dashboard online tại URL: `https://your-username-credit-risk-analytics.streamlit.app`
- ✅ Người dùng có thể tương tác trực tiếp
- ✅ Miễn phí 100%
- ✅ Tự động update khi push code mới

---

## 📋 Bước 1: Chuẩn Bị Files

### ✅ Files đã có sẵn:
- `app.py` - Dashboard code
- `requirements.txt` - Dependencies
- `README.md` - Documentation

### 📝 Cần tạo thêm:

**1. Tạo file `.streamlit/config.toml`** (đã có thư mục .streamlit)

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
port = 8501
```

**2. Kiểm tra `requirements.txt`** (đã OK)

---

## 📤 Bước 2: Push Code Lên GitHub

### Option A: Nếu chưa có Git repository

```bash
# 1. Khởi tạo Git (nếu chưa có)
cd C:\Users\ASUS\credit-risk-analytics
git init

# 2. Add files
git add .

# 3. Commit
git commit -m "Add interactive Streamlit dashboard"

# 4. Tạo repository trên GitHub
# Vào https://github.com/new
# Tên repo: credit-risk-analytics
# Public repository

# 5. Push lên GitHub
git remote add origin https://github.com/YOUR_USERNAME/credit-risk-analytics.git
git branch -M main
git push -u origin main
```

### Option B: Nếu đã có Git repository

```bash
cd C:\Users\ASUS\credit-risk-analytics
git add dashboards/
git commit -m "Add interactive Streamlit dashboard"
git push
```

---

## ☁️ Bước 3: Deploy Lên Streamlit Cloud

### 1. Đăng ký Streamlit Cloud (MIỄN PHÍ)

- Vào: https://share.streamlit.io
- Click "Sign up" hoặc "Continue with GitHub"
- Đăng nhập bằng GitHub account

### 2. Deploy App

1. Click **"New app"** hoặc **"Create app"**

2. Điền thông tin:
   - **Repository:** `your-username/credit-risk-analytics`
   - **Branch:** `main`
   - **Main file path:** `dashboards/app.py`
   - **App URL:** `credit-risk-analytics` (hoặc tên bạn muốn)

3. Click **"Deploy!"**

### 3. Đợi Deploy (2-3 phút)

Streamlit Cloud sẽ:
- Clone repository
- Install dependencies từ `requirements.txt`
- Chạy `app.py`
- Tạo public URL

---

## 🎉 Bước 4: Truy Cập Dashboard

### URL của bạn sẽ là:
```
https://your-username-credit-risk-analytics.streamlit.app
```

hoặc

```
https://credit-risk-analytics-abc123.streamlit.app
```

### ✅ Dashboard đã LIVE và tương tác được!

Người dùng có thể:
- ✅ Chọn trang từ sidebar
- ✅ Tương tác với charts (hover, zoom, pan)
- ✅ Dùng filters
- ✅ Export CSV
- ✅ Xem real-time metrics

---

## 🔧 Troubleshooting

### Lỗi: "No module named 'streamlit'"
**Giải pháp:** Kiểm tra `requirements.txt` có đầy đủ:
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
```

### Lỗi: "File not found: data/..."
**Giải pháp:** Dashboard tự động generate synthetic data nếu không có file. Không cần lo!

### Lỗi: Build failed
**Giải pháp:** 
1. Check logs trên Streamlit Cloud
2. Đảm bảo `requirements.txt` không có version conflicts
3. Test local trước: `streamlit run dashboards/app.py`

---

## 🎨 Customization

### Thay đổi theme:
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"  # Đỏ
backgroundColor = "#0E1117"  # Dark mode
```

### Update dashboard:
```bash
# Sửa code trong app.py
git add dashboards/app.py
git commit -m "Update dashboard"
git push
# Streamlit Cloud tự động redeploy!
```

---

## 📊 Demo Dashboard Features

Khi dashboard đã live, người dùng có thể:

### 🏠 Executive Summary
- Xem Portfolio KPIs
- Tương tác với charts
- Hover để xem chi tiết

### ⚠️ Risk Monitoring
- Phân tích risk metrics
- Filter theo grade
- Zoom vào charts

### 👥 Customer Segments
- Chọn segment từ dropdown
- So sánh segments
- Export data

### 📈 Cohort Analysis
- Xem vintage performance
- Track trends theo time

### 🤖 Model Performance
- So sánh models
- Xem feature importance

### 📋 Data Explorer
- Filter data real-time
- Download CSV
- Explore statistics

---

## 🎯 Kết Luận

**Sau khi deploy:**
- ✅ Dashboard ONLINE và INTERACTIVE
- ✅ Public URL để share
- ✅ Miễn phí vĩnh viễn
- ✅ Auto-update khi push code

**Thời gian:**
- Push to GitHub: 2 phút
- Deploy on Streamlit Cloud: 3 phút
- **Total: 5 phút → Dashboard LIVE!**

---

## 📧 Support

Nếu cần help deploy:
- Email: tuyetngth2558@gmail.com
- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
