# Streamlit Dashboard Deployment Guide

## 🚀 Quick Start (Local)

### 1. Install Dependencies
```bash
cd dashboards
pip install -r requirements.txt
```

### 2. Run Dashboard
```bash
# Option A: Direct command
streamlit run app.py

# Option B: Using batch script (Windows)
.\run_dashboard.bat
```

### 3. Access Dashboard
Open browser to: `http://localhost:8501`

---

## ☁️ Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Advantages:**
- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Easy GitHub integration
- ✅ Auto-redeploy on push

**Steps:**

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add Streamlit dashboard"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `dashboards/app.py`
   - Click "Deploy"

3. **Access your app:**
   - URL: `https://your-username-credit-risk-analytics.streamlit.app`

**Configuration:**
Create `dashboards/.streamlit/secrets.toml` for sensitive data (not committed to Git):
```toml
# Database credentials (if needed)
[postgres]
host = "your-host"
port = 5432
database = "your-db"
user = "your-user"
password = "your-password"
```

---

### Option 2: Heroku

**Advantages:**
- ✅ Free tier available
- ✅ Custom domain support
- ✅ Add-ons ecosystem

**Steps:**

1. **Create required files:**

`Procfile`:
```
web: sh setup.sh && streamlit run dashboards/app.py
```

`setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

2. **Deploy:**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

3. **Access:**
```
https://your-app-name.herokuapp.com
```

---

### Option 3: Docker + Any Cloud

**Advantages:**
- ✅ Portable
- ✅ Works on AWS, GCP, Azure
- ✅ Scalable

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY dashboards/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY dashboards/ .
COPY data/ ../data/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build & Run:**
```bash
# Build image
docker build -t credit-risk-dashboard .

# Run container
docker run -p 8501:8501 credit-risk-dashboard
```

**Deploy to Cloud:**
- **AWS ECS/Fargate:** Push to ECR, create service
- **Google Cloud Run:** `gcloud run deploy`
- **Azure Container Instances:** `az container create`

---

## 🔒 Security Best Practices

### 1. Environment Variables
Never hardcode credentials. Use environment variables:

```python
import os
import streamlit as st

# In app.py
db_password = os.getenv('DB_PASSWORD') or st.secrets.get('DB_PASSWORD')
```

### 2. Authentication (Optional)
Add basic auth using `streamlit-authenticator`:

```bash
pip install streamlit-authenticator
```

```python
import streamlit_authenticator as stauth

# In app.py
authenticator = stauth.Authenticate(
    credentials,
    'credit_risk_dashboard',
    'auth_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show dashboard
    pass
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

### 3. Rate Limiting
For production, add rate limiting:
- Use Cloudflare (free tier)
- Implement API rate limits
- Add CAPTCHA for sensitive operations

---

## 📊 Performance Optimization

### 1. Data Caching
Already implemented with `@st.cache_data`:
```python
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')
```

### 2. Lazy Loading
Load data only when needed:
```python
if page == "Executive Summary":
    df = load_data()  # Only load when viewing this page
```

### 3. Pagination
For large datasets:
```python
# Show 100 rows at a time
page_size = 100
page_num = st.number_input('Page', min_value=1, max_value=len(df)//page_size)
st.dataframe(df.iloc[(page_num-1)*page_size:page_num*page_size])
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: data file not found"
**Solution:**
- Ensure data files are in correct location
- Dashboard will auto-generate synthetic data if files missing
- Check file paths in `load_data()` function

### Issue: Port 8501 already in use
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Dashboard is slow
**Solutions:**
- Reduce data size (sample data)
- Add more caching
- Optimize queries
- Use pagination

---

## 📈 Monitoring & Analytics

### Add Google Analytics
In `app.py`:
```python
# Add to <head>
st.markdown("""
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'GA_MEASUREMENT_ID');
    </script>
""", unsafe_allow_html=True)
```

### Streamlit Analytics
Built-in analytics available on Streamlit Cloud:
- Page views
- User sessions
- Error tracking

---

## 🎯 Next Steps

### Enhancements:
1. **Database Integration:** Connect to PostgreSQL/MySQL
2. **Real-time Updates:** Auto-refresh data
3. **Export Features:** PDF reports, Excel downloads
4. **Advanced Filters:** Date ranges, multi-criteria
5. **User Management:** Role-based access control
6. **API Integration:** Connect to external data sources

### Production Checklist:
- [ ] Add authentication
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Add error tracking (Sentry)
- [ ] Set up CI/CD pipeline
- [ ] Load testing
- [ ] Security audit
- [ ] Documentation

---

## 📧 Support

For deployment issues or questions:

**Email:** tuyetngth2558@gmail.com  
**LinkedIn:** [linkedin.com/in/tuyet-nguyen-5a099a29a](https://www.linkedin.com/in/tuyet-nguyen-5a099a29a/)

---

**Happy Deploying! 🚀**
