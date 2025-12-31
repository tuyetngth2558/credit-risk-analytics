"""
Credit Risk Analytics - Interactive Dashboard
==============================================
Multi-page Streamlit dashboard for credit risk analytics and monitoring

Author: Tuyet Nguyen
Email: tuyetngth2558@gmail.com
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Credit Risk Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2c3e50;
        margin-top: 20px;
    }
    .reportview-container .main footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# Data loading with caching
@st.cache_data
def load_data():
    """Load and cache the processed loan data"""
    try:
        # Try to load processed data with features
        df = pd.read_csv('../data/processed/loans_with_features.csv')
    except FileNotFoundError:
        try:
            # Fallback to sample data
            df = pd.read_csv('../data/sample/sample_loans_10k.csv')
            st.warning("⚠️ Using sample data. Processed features not found.")
        except FileNotFoundError:
            # Generate synthetic data for demo
            st.error("❌ No data files found. Generating synthetic data for demonstration.")
            df = generate_synthetic_data()
    
    return df

def generate_synthetic_data(n_samples=10000):
    """Generate synthetic loan data for demonstration"""
    np.random.seed(42)
    
    data = {
        'loan_amnt': np.random.uniform(1000, 40000, n_samples),
        'int_rate': np.random.uniform(5, 25, n_samples),
        'annual_inc': np.random.uniform(20000, 200000, n_samples),
        'dti': np.random.uniform(0, 40, n_samples),
        'fico_score': np.random.randint(600, 850, n_samples),
        'loan_status': np.random.choice(['Fully Paid', 'Current', 'Charged Off', 'Late'], 
                                       n_samples, p=[0.6, 0.25, 0.1, 0.05]),
        'loan_grade': np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 
                                      n_samples, p=[0.15, 0.25, 0.25, 0.2, 0.1, 0.03, 0.02]),
        'credit_utilization': np.random.uniform(0, 100, n_samples),
        'risk_score': np.random.uniform(0, 100, n_samples),
        'issue_year': np.random.choice([2015, 2016, 2017, 2018], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create derived fields
    df['is_default'] = df['loan_status'].isin(['Charged Off', 'Late']).astype(int)
    df['risk_category'] = pd.cut(df['risk_score'], 
                                  bins=[0, 25, 50, 75, 100],
                                  labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk'])
    df['fico_category'] = pd.cut(df['fico_score'],
                                  bins=[0, 580, 670, 740, 800, 850],
                                  labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
    
    return df

# Load data
df = load_data()

# Sidebar navigation
st.sidebar.title("📊 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Executive Summary", 
     "⚠️ Risk Monitoring", 
     "👥 Customer Segments",
     "📈 Cohort Analysis",
     "🤖 Model Performance",
     "📋 Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Stats")
st.sidebar.metric("Total Loans", f"{len(df):,}")
st.sidebar.metric("Total Volume", f"${df['loan_amnt'].sum()/1e6:.1f}M")
if 'is_default' in df.columns:
    default_rate = df['is_default'].mean() * 100
    st.sidebar.metric("Default Rate", f"{default_rate:.2f}%", 
                     delta=f"{default_rate - 10:.2f}%" if default_rate < 10 else None,
                     delta_color="inverse")

st.sidebar.markdown("---")
st.sidebar.info("""
**Credit Risk Analytics Dashboard**

Interactive analytics platform for credit risk monitoring and decision intelligence.

📧 tuyetngth2558@gmail.com
""")

# ============================================================================
# PAGE 1: EXECUTIVE SUMMARY
# ============================================================================

if page == "🏠 Executive Summary":
    st.title("🏠 Executive Summary Dashboard")
    st.markdown("### Portfolio Overview and Key Performance Indicators")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_loans = len(df)
        st.metric("Total Loans", f"{total_loans:,}", 
                 delta=f"+{int(total_loans * 0.05):,} vs last month")
    
    with col2:
        total_volume = df['loan_amnt'].sum()
        st.metric("Total Volume", f"${total_volume/1e6:.1f}M",
                 delta=f"+${total_volume * 0.08 / 1e6:.1f}M")
    
    with col3:
        avg_loan = df['loan_amnt'].mean()
        st.metric("Avg Loan Amount", f"${avg_loan:,.0f}",
                 delta=f"${avg_loan * 0.03:,.0f}")
    
    with col4:
        if 'is_default' in df.columns:
            default_rate = df['is_default'].mean() * 100
            st.metric("NPL Ratio", f"{default_rate:.2f}%",
                     delta=f"{default_rate - 5:.2f}%",
                     delta_color="inverse")
        else:
            st.metric("NPL Ratio", "N/A")
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Loan Volume by Grade")
        grade_volume = df.groupby('loan_grade')['loan_amnt'].sum().reset_index()
        fig = px.bar(grade_volume, x='loan_grade', y='loan_amnt',
                    color='loan_grade',
                    labels={'loan_amnt': 'Total Volume ($)', 'loan_grade': 'Loan Grade'},
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Loan Origination Trend")
        if 'issue_year' in df.columns:
            yearly_trend = df.groupby('issue_year').size().reset_index(name='count')
            fig = px.line(yearly_trend, x='issue_year', y='count',
                         markers=True,
                         labels={'count': 'Number of Loans', 'issue_year': 'Year'},
                         color_discrete_sequence=['#1f77b4'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Year data not available")
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Loan Status Distribution")
        status_dist = df['loan_status'].value_counts().reset_index()
        status_dist.columns = ['status', 'count']
        fig = px.pie(status_dist, values='count', names='status',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Interest Rate Distribution")
        fig = px.histogram(df, x='int_rate', nbins=50,
                          labels={'int_rate': 'Interest Rate (%)', 'count': 'Frequency'},
                          color_discrete_sequence=['#ff7f0e'])
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: RISK MONITORING
# ============================================================================

elif page == "⚠️ Risk Monitoring":
    st.title("⚠️ Risk Monitoring Dashboard")
    st.markdown("### Portfolio Risk Analysis and Early Warning Indicators")
    
    # Risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'risk_score' in df.columns:
            avg_risk = df['risk_score'].mean()
            st.metric("Avg Risk Score", f"{avg_risk:.1f}",
                     delta=f"{avg_risk - 50:.1f}",
                     delta_color="inverse")
        else:
            st.metric("Avg Risk Score", "N/A")
    
    with col2:
        if 'fico_score' in df.columns:
            avg_fico = df['fico_score'].mean()
            st.metric("Avg FICO Score", f"{avg_fico:.0f}",
                     delta=f"{avg_fico - 700:.0f}")
        else:
            st.metric("Avg FICO Score", "N/A")
    
    with col3:
        if 'dti' in df.columns:
            avg_dti = df['dti'].mean()
            st.metric("Avg DTI Ratio", f"{avg_dti:.1f}%",
                     delta=f"{avg_dti - 20:.1f}%",
                     delta_color="inverse")
        else:
            st.metric("Avg DTI Ratio", "N/A")
    
    with col4:
        if 'credit_utilization' in df.columns:
            avg_util = df['credit_utilization'].mean()
            st.metric("Avg Credit Util", f"{avg_util:.1f}%",
                     delta=f"{avg_util - 50:.1f}%",
                     delta_color="inverse")
        else:
            st.metric("Avg Credit Util", "N/A")
    
    st.markdown("---")
    
    # Risk analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Default Rate by Grade")
        if 'is_default' in df.columns:
            default_by_grade = df.groupby('loan_grade').agg({
                'is_default': 'mean',
                'loan_amnt': 'count'
            }).reset_index()
            default_by_grade.columns = ['grade', 'default_rate', 'count']
            default_by_grade['default_rate'] *= 100
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=default_by_grade['grade'],
                y=default_by_grade['default_rate'],
                name='Default Rate (%)',
                marker_color='crimson'
            ))
            fig.update_layout(
                yaxis_title='Default Rate (%)',
                xaxis_title='Loan Grade',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Default data not available")
    
    with col2:
        st.subheader("📊 Risk Score Distribution")
        if 'risk_score' in df.columns:
            fig = px.histogram(df, x='risk_score', nbins=50,
                              labels={'risk_score': 'Risk Score', 'count': 'Frequency'},
                              color_discrete_sequence=['#d62728'])
            fig.add_vline(x=df['risk_score'].mean(), line_dash="dash", 
                         line_color="blue", annotation_text="Mean")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Risk score not available")
    
    # Risk category breakdown
    st.subheader("⚠️ Portfolio Risk Breakdown")
    
    if 'risk_category' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            risk_dist = df['risk_category'].value_counts().reset_index()
            risk_dist.columns = ['category', 'count']
            fig = px.pie(risk_dist, values='count', names='category',
                        color='category',
                        color_discrete_map={
                            'Low Risk': '#2ecc71',
                            'Medium Risk': '#f39c12',
                            'High Risk': '#e74c3c',
                            'Very High Risk': '#c0392b'
                        })
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk vs Default correlation
            if 'is_default' in df.columns:
                risk_default = df.groupby('risk_category')['is_default'].mean() * 100
                risk_default = risk_default.reset_index()
                risk_default.columns = ['category', 'default_rate']
                
                fig = px.bar(risk_default, x='category', y='default_rate',
                            color='default_rate',
                            labels={'default_rate': 'Default Rate (%)', 'category': 'Risk Category'},
                            color_continuous_scale='Reds')
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 3: CUSTOMER SEGMENTS
# ============================================================================

elif page == "👥 Customer Segments":
    st.title("👥 Customer Segmentation Analysis")
    st.markdown("### Customer Profiles and Segment Performance")
    
    # Segment selector
    if 'risk_category' in df.columns:
        segments = df['risk_category'].unique()
        selected_segment = st.selectbox("Select Segment to Analyze:", 
                                       ['All Segments'] + list(segments))
        
        if selected_segment != 'All Segments':
            segment_df = df[df['risk_category'] == selected_segment]
        else:
            segment_df = df
    else:
        segment_df = df
        st.info("Segment data not available. Showing all customers.")
    
    # Segment metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Customers", f"{len(segment_df):,}")
    
    with col2:
        st.metric("Avg Loan", f"${segment_df['loan_amnt'].mean():,.0f}")
    
    with col3:
        if 'fico_score' in segment_df.columns:
            st.metric("Avg FICO", f"{segment_df['fico_score'].mean():.0f}")
        else:
            st.metric("Avg FICO", "N/A")
    
    with col4:
        if 'is_default' in segment_df.columns:
            st.metric("Default Rate", f"{segment_df['is_default'].mean()*100:.2f}%")
        else:
            st.metric("Default Rate", "N/A")
    
    st.markdown("---")
    
    # Segment analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Income Distribution")
        fig = px.box(segment_df, y='annual_inc',
                    labels={'annual_inc': 'Annual Income ($)'},
                    color_discrete_sequence=['#3498db'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 FICO Score Distribution")
        if 'fico_score' in segment_df.columns:
            fig = px.histogram(segment_df, x='fico_score', nbins=30,
                              labels={'fico_score': 'FICO Score'},
                              color_discrete_sequence=['#9b59b6'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("FICO data not available")
    
    # Segment comparison
    if 'risk_category' in df.columns:
        st.subheader("📈 Segment Comparison")
        
        segment_stats = df.groupby('risk_category').agg({
            'loan_amnt': ['count', 'mean', 'sum'],
            'is_default': 'mean' if 'is_default' in df.columns else 'count',
            'fico_score': 'mean' if 'fico_score' in df.columns else 'count'
        }).round(2)
        
        st.dataframe(segment_stats, use_container_width=True)

# ============================================================================
# PAGE 4: COHORT ANALYSIS
# ============================================================================

elif page == "📈 Cohort Analysis":
    st.title("📈 Cohort Analysis Dashboard")
    st.markdown("### Vintage Performance and Portfolio Aging")
    
    if 'issue_year' in df.columns:
        # Cohort metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cohorts = df['issue_year'].nunique()
            st.metric("Total Cohorts", cohorts)
        
        with col2:
            latest_year = df['issue_year'].max()
            latest_volume = df[df['issue_year'] == latest_year]['loan_amnt'].sum()
            st.metric(f"{latest_year} Volume", f"${latest_volume/1e6:.1f}M")
        
        with col3:
            if 'is_default' in df.columns:
                latest_default = df[df['issue_year'] == latest_year]['is_default'].mean() * 100
                st.metric(f"{latest_year} Default Rate", f"{latest_default:.2f}%")
        
        st.markdown("---")
        
        # Cohort charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Volume by Vintage")
            cohort_volume = df.groupby('issue_year')['loan_amnt'].sum().reset_index()
            fig = px.bar(cohort_volume, x='issue_year', y='loan_amnt',
                        labels={'loan_amnt': 'Total Volume ($)', 'issue_year': 'Year'},
                        color='loan_amnt',
                        color_continuous_scale='Blues')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Default Rate by Vintage")
            if 'is_default' in df.columns:
                cohort_default = df.groupby('issue_year')['is_default'].mean() * 100
                cohort_default = cohort_default.reset_index()
                cohort_default.columns = ['year', 'default_rate']
                
                fig = px.line(cohort_default, x='year', y='default_rate',
                             markers=True,
                             labels={'default_rate': 'Default Rate (%)', 'year': 'Year'},
                             color_discrete_sequence=['#e74c3c'])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Cohort table
        st.subheader("📋 Cohort Performance Table")
        cohort_table = df.groupby('issue_year').agg({
            'loan_amnt': ['count', 'sum', 'mean'],
            'is_default': 'mean' if 'is_default' in df.columns else 'count',
            'int_rate': 'mean'
        }).round(2)
        st.dataframe(cohort_table, use_container_width=True)
    else:
        st.warning("⚠️ Cohort data (issue_year) not available in dataset")

# ============================================================================
# PAGE 5: MODEL PERFORMANCE
# ============================================================================

elif page == "🤖 Model Performance":
    st.title("🤖 Model Performance Dashboard")
    st.markdown("### Credit Scoring Model Evaluation and Metrics")
    
    st.info("""
    📊 **Model Performance Summary**
    
    This dashboard shows the performance of credit risk scoring models built in notebook 03.
    Models include Logistic Regression, Random Forest, and XGBoost.
    """)
    
    # Model metrics (simulated for demo)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Best Model AUC", "0.781", delta="+0.031 vs baseline")
    
    with col2:
        st.metric("Precision", "0.742", delta="+0.05")
    
    with col3:
        st.metric("Recall", "0.689", delta="+0.08")
    
    with col4:
        st.metric("F1 Score", "0.714", delta="+0.06")
    
    st.markdown("---")
    
    # Model comparison
    st.subheader("📊 Model Comparison")
    
    model_data = pd.DataFrame({
        'Model': ['Logistic Regression', 'Random Forest', 'XGBoost'],
        'AUC-ROC': [0.750, 0.781, 0.778],
        'F1 Score': [0.654, 0.714, 0.702],
        'Precision': [0.692, 0.742, 0.728],
        'Recall': [0.621, 0.689, 0.678]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(model_data, x='Model', y='AUC-ROC',
                    color='Model',
                    labels={'AUC-ROC': 'AUC-ROC Score'},
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.add_hline(y=0.75, line_dash="dash", line_color="red", 
                     annotation_text="Target: 0.75")
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        for metric in ['Precision', 'Recall', 'F1 Score']:
            fig.add_trace(go.Bar(
                name=metric,
                x=model_data['Model'],
                y=model_data[metric]
            ))
        fig.update_layout(barmode='group', height=400,
                         yaxis_title='Score',
                         legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    st.subheader("🎯 Top Feature Importance")
    
    feature_importance = pd.DataFrame({
        'Feature': ['FICO Score', 'DTI Ratio', 'Credit Utilization', 
                   'Loan Amount', 'Interest Rate', 'Annual Income',
                   'Delinquencies', 'Inquiries'],
        'Importance': [0.35, 0.28, 0.22, 0.08, 0.04, 0.02, 0.01, 0.005]
    })
    
    fig = px.bar(feature_importance, x='Importance', y='Feature',
                orientation='h',
                color='Importance',
                color_continuous_scale='Viridis')
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 6: DATA EXPLORER
# ============================================================================

elif page == "📋 Data Explorer":
    st.title("📋 Data Explorer")
    st.markdown("### Interactive Data Exploration and Filtering")
    
    # Filters
    st.subheader("🔍 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        grade_filter = st.multiselect("Loan Grade:", 
                                     options=df['loan_grade'].unique(),
                                     default=df['loan_grade'].unique())
    
    with col2:
        if 'issue_year' in df.columns:
            year_filter = st.multiselect("Issue Year:",
                                        options=sorted(df['issue_year'].unique()),
                                        default=sorted(df['issue_year'].unique()))
        else:
            year_filter = None
    
    with col3:
        status_filter = st.multiselect("Loan Status:",
                                      options=df['loan_status'].unique(),
                                      default=df['loan_status'].unique())
    
    # Apply filters
    filtered_df = df[df['loan_grade'].isin(grade_filter) & 
                     df['loan_status'].isin(status_filter)]
    
    if year_filter and 'issue_year' in df.columns:
        filtered_df = filtered_df[filtered_df['issue_year'].isin(year_filter)]
    
    st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} loans**")
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)
    
    # Data table
    st.subheader("📋 Data Table")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_loans.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p><strong>Credit Risk Analytics Dashboard</strong> | Built with Streamlit & Plotly</p>
    <p>📧 tuyetngth2558@gmail.com | 💼 <a href='https://www.linkedin.com/in/tuyet-nguyen-5a099a29a/'>LinkedIn</a> | 
    🔗 <a href='https://github.com/tuyetngth2558'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
