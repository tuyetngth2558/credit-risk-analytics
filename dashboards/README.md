# Credit Risk Analytics - Interactive Dashboard

## 🌐 LIVE DEMO (Deploy to Cloud)

**Want to see it in action?** Deploy this dashboard to Streamlit Cloud in 5 minutes!

👉 **[Follow Deployment Guide](DEPLOY_TO_CLOUD.md)**

Your dashboard will be live at: `https://your-username-credit-risk-analytics.streamlit.app`

---

## 🎯 Overview

Interactive Streamlit dashboard for credit risk analytics, portfolio monitoring, and decision intelligence.

![Dashboard Preview](risk_monitoring.png)

## 🚀 Features

### 📊 Multi-Page Dashboard

1. **Executive Summary**
   - Portfolio KPIs (Total Loans, Volume, NPL Ratio)
   - Loan volume by grade
   - Origination trends
   - Status distribution

2. **Risk Monitoring**
   - Risk score analytics
   - Default rate by grade
   - FICO and DTI distributions
   - Portfolio risk breakdown

3. **Customer Segments**
   - Segment performance analysis
   - Customer profiling
   - Income and FICO distributions
   - Segment comparison tables

4. **Cohort Analysis**
   - Vintage performance tracking
   - Default rate trends by cohort
   - Portfolio aging analysis
   - Cohort comparison tables

5. **Model Performance**
   - ML model comparison (Logistic Regression, Random Forest, XGBoost)
   - AUC-ROC, Precision, Recall, F1 scores
   - Feature importance visualization
   - Model evaluation metrics

6. **Data Explorer**
   - Interactive filtering
   - Summary statistics
   - Data table view
   - CSV export functionality

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Navigate to dashboard directory:**
```bash
cd dashboards
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🏃 Running the Dashboard

### Option 1: Using Streamlit directly
```bash
streamlit run app.py
```

### Option 2: Using Python
```bash
python -m streamlit run app.py
```

### Option 3: Using the run script (Windows)
```bash
.\run_dashboard.bat
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## 📊 Data Requirements

The dashboard can work with:

1. **Processed data** (recommended): `../data/processed/loans_with_features.csv`
   - Generated from notebook 02 (feature engineering)
   - Includes all engineered features

2. **Sample data** (fallback): `../data/sample/sample_loans_10k.csv`
   - 10K sample loans for testing

3. **Synthetic data** (demo mode): Auto-generated if no data files found

## 🎨 Dashboard Features

### Interactive Elements
- ✅ Multi-select filters
- ✅ Dynamic charts (Plotly)
- ✅ Responsive layout
- ✅ Real-time data updates
- ✅ CSV export
- ✅ Metric cards with deltas

### Visualizations
- 📊 Bar charts
- 📈 Line charts
- 🥧 Pie charts
- 📦 Box plots
- 📉 Histograms
- 🔥 Heatmaps (via correlation)

## 🔧 Customization

### Modify Page Content
Edit `app.py` and update the corresponding page section:
```python
if page == "🏠 Executive Summary":
    # Your custom code here
```

### Add New Pages
1. Add new page option in sidebar:
```python
page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Executive Summary", "Your New Page"]
)
```

2. Add page logic:
```python
elif page == "Your New Page":
    st.title("Your New Page")
    # Your code here
```

### Change Color Scheme
Modify the custom CSS in the `st.markdown()` section at the top of `app.py`

## 📱 Deployment Options

### 1. Streamlit Cloud (Recommended - Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

### 2. Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### 3. Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🎓 Skills Demonstrated

- ✅ **Streamlit Development**: Multi-page apps, caching, state management
- ✅ **Data Visualization**: Plotly interactive charts, custom styling
- ✅ **Python Programming**: Pandas, NumPy, data processing
- ✅ **UI/UX Design**: Responsive layouts, intuitive navigation
- ✅ **Dashboard Analytics**: KPIs, metrics, business intelligence

## 📧 Support

**Author:** Tuyet Nguyen  
**Email:** tuyetngth2558@gmail.com  
**LinkedIn:** [linkedin.com/in/tuyet-nguyen-5a099a29a](https://www.linkedin.com/in/tuyet-nguyen-5a099a29a/)  
**GitHub:** [github.com/tuyetngth2558](https://github.com/tuyetngth2558)

## 📄 License

MIT License - Free to use for learning and portfolio purposes.

---

**Built with ❤️ using Streamlit, Plotly, and Python**
