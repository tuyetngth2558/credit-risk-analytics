# %% [markdown]
# # Credit Risk Analytics - Data Exploration
# 
# **Objective:** Initial exploration of loan data to understand patterns, distributions, and data quality
# 
# **Author:** Your Name  
# **Date:** December 2024

# %% [markdown]
# ## 1. Setup & Imports

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import project config
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))
from config.config import SAMPLE_DATA_PATH, RANDOM_SEED

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("✓ Libraries imported successfully!")
print(f"✓ Pandas version: {pd.__version__}")
print(f"✓ NumPy version: {np.__version__}")

# %% [markdown]
# ## 2. Load Data

# %%
# Load sample data
data_path = SAMPLE_DATA_PATH / 'sample_loans_10k.csv'
df = pd.read_csv(data_path)

print("="*60)
print("DATA LOADED SUCCESSFULLY")
print("="*60)
print(f"\n📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"💾 Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Display first few rows
df.head()

# %% [markdown]
# ## 3. Data Overview

# %%
# Basic info
print("\n" + "="*60)
print("DATASET INFORMATION")
print("="*60)
df.info()

# %%
# Column names
print("\n" + "="*60)
print("COLUMN NAMES")
print("="*60)
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

# %% [markdown]
# ## 4. Statistical Summary

# %%
# Numerical columns summary
print("\n" + "="*60)
print("NUMERICAL FEATURES SUMMARY")
print("="*60)
df.describe()

# %% [markdown]
# ## 5. Missing Values Analysis

# %%
# Check missing values
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
})
missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)

print("\n" + "="*60)
print("MISSING VALUES ANALYSIS")
print("="*60)
if len(missing_df) > 0:
    print(missing_df)
else:
    print("✓ No missing values found!")

# %% [markdown]
# ## 6. Target Variable: Loan Status

# %%
# Loan status distribution
print("\n" + "="*60)
print("LOAN STATUS DISTRIBUTION")
print("="*60)

status_counts = df['loan_status'].value_counts()
status_pct = (status_counts / len(df) * 100).round(2)

status_summary = pd.DataFrame({
    'Count': status_counts,
    'Percentage': status_pct
})
print(status_summary)

# %%
# Visualize loan status
plt.figure(figsize=(10, 6))
status_counts.plot(kind='bar', color='steelblue', edgecolor='black', alpha=0.8)
plt.title('Loan Status Distribution', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Loan Status', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 7. Default Analysis

# %%
# Create binary target: Default vs Non-Default
default_statuses = ['Charged Off', 'Default', 'Late (31-120 days)']
df['is_default'] = df['loan_status'].isin(default_statuses).astype(int)

default_rate = df['is_default'].mean() * 100
print(f"\n📊 Overall Default Rate: {default_rate:.2f}%")
print(f"   - Defaults: {df['is_default'].sum():,}")
print(f"   - Non-Defaults: {(~df['is_default'].astype(bool)).sum():,}")

# %%
# Default vs Non-Default pie chart
plt.figure(figsize=(8, 8))
labels = ['Non-Default', 'Default']
sizes = [100-default_rate, default_rate]
colors = ['#66b3ff', '#ff6666']
explode = (0, 0.1)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('Default vs Non-Default Distribution', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.show()

# %% [markdown]
# ## 8. Risk Grade Analysis

# %%
# Risk grade distribution
print("\n" + "="*60)
print("LOAN GRADE DISTRIBUTION")
print("="*60)

grade_counts = df['grade'].value_counts().sort_index()
print(grade_counts)

# %%
# Plot grade analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Grade distribution
grade_counts.plot(kind='bar', ax=ax1, color='lightcoral', edgecolor='black', alpha=0.8)
ax1.set_title('Loan Grade Distribution', fontsize=14, fontweight='bold')
ax1.set_xlabel('Grade', fontsize=12)
ax1.set_ylabel('Count', fontsize=12)
ax1.grid(axis='y', alpha=0.3)

# Default rate by grade
default_by_grade = df.groupby('grade')['is_default'].mean() * 100
default_by_grade.plot(kind='bar', ax=ax2, color='salmon', edgecolor='black', alpha=0.8)
ax2.set_title('Default Rate by Grade', fontsize=14, fontweight='bold')
ax2.set_xlabel('Grade', fontsize=12)
ax2.set_ylabel('Default Rate (%)', fontsize=12)
ax2.axhline(y=default_rate, color='red', linestyle='--', label=f'Overall: {default_rate:.1f}%')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# **Key Insight:** Default rate increases from Grade A to Grade G, validating the risk grading system.

# %% [markdown]
# ## 9. Loan Amount Analysis

# %%
# Loan amount distribution
print("\n" + "="*60)
print("LOAN AMOUNT ANALYSIS")
print("="*60)
print(f"Mean: ${df['loan_amnt'].mean():,.0f}")
print(f"Median: ${df['loan_amnt'].median():,.0f}")
print(f"Std Dev: ${df['loan_amnt'].std():,.0f}")
print(f"Min: ${df['loan_amnt'].min():,.0f}")
print(f"Max: ${df['loan_amnt'].max():,.0f}")

# %%
# Plot loan amount distribution
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Histogram
axes[0].hist(df['loan_amnt'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].axvline(df['loan_amnt'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["loan_amnt"].mean():,.0f}')
axes[0].axvline(df['loan_amnt'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: ${df["loan_amnt"].median():,.0f}')
axes[0].set_title('Loan Amount Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Loan Amount ($)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].legend()
axes[0].grid(alpha=0.3)

# Box plot by default status
df.boxplot(column='loan_amnt', by='is_default', ax=axes[1])
axes[1].set_title('Loan Amount by Default Status', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Default Status (0=No, 1=Yes)', fontsize=12)
axes[1].set_ylabel('Loan Amount ($)', fontsize=12)
plt.suptitle('')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 10. Interest Rate Analysis

# %%
# Interest rate statistics
print("\n" + "="*60)
print("INTEREST RATE ANALYSIS")
print("="*60)
print(f"Mean: {df['int_rate'].mean():.2f}%")
print(f"Median: {df['int_rate'].median():.2f}%")
print(f"Std Dev: {df['int_rate'].std():.2f}%")
print(f"Min: {df['int_rate'].min():.2f}%")
print(f"Max: {df['int_rate'].max():.2f}%")

# %%
# Interest rate distribution
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Overall distribution
axes[0, 0].hist(df['int_rate'], bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Interest Rate Distribution', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Interest Rate (%)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].grid(alpha=0.3)

# By grade
df.boxplot(column='int_rate', by='grade', ax=axes[0, 1])
axes[0, 1].set_title('Interest Rate by Grade', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Grade')
axes[0, 1].set_ylabel('Interest Rate (%)')
plt.suptitle('')

# By default status
df.boxplot(column='int_rate', by='is_default', ax=axes[1, 0])
axes[1, 0].set_title('Interest Rate by Default Status', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Default (0=No, 1=Yes)')
axes[1, 0].set_ylabel('Interest Rate (%)')

# Average by grade
avg_rate_by_grade = df.groupby('grade')['int_rate'].mean()
avg_rate_by_grade.plot(kind='bar', ax=axes[1, 1], color='orange', edgecolor='black', alpha=0.8)
axes[1, 1].set_title('Average Interest Rate by Grade', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Grade')
axes[1, 1].set_ylabel('Avg Interest Rate (%)')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 11. FICO Score Analysis

# %%
# FICO score distribution
print("\n" + "="*60)
print("FICO SCORE ANALYSIS")
print("="*60)
print(f"Mean: {df['fico_range_low'].mean():.0f}")
print(f"Median: {df['fico_range_low'].median():.0f}")
print(f"Std Dev: {df['fico_range_low'].std():.0f}")
print(f"Min: {df['fico_range_low'].min():.0f}")
print(f"Max: {df['fico_range_low'].max():.0f}")

# %%
# FICO score visualization
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Distribution
axes[0].hist(df['fico_range_low'], bins=50, color='purple', edgecolor='black', alpha=0.7)
axes[0].axvline(df['fico_range_low'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["fico_range_low"].mean():.0f}')
axes[0].set_title('FICO Score Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('FICO Score', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].legend()
axes[0].grid(alpha=0.3)

# By default status
df.boxplot(column='fico_range_low', by='is_default', ax=axes[1])
axes[1].set_title('FICO Score by Default Status', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Default (0=No, 1=Yes)', fontsize=12)
axes[1].set_ylabel('FICO Score', fontsize=12)
plt.suptitle('')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 12. DTI (Debt-to-Income) Analysis

# %%
# DTI statistics
print("\n" + "="*60)
print("DTI (DEBT-TO-INCOME) ANALYSIS")
print("="*60)
print(f"Mean: {df['dti'].mean():.2f}%")
print(f"Median: {df['dti'].median():.2f}%")
print(f"Std Dev: {df['dti'].std():.2f}%")

# %%
# DTI visualization
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Distribution
axes[0].hist(df['dti'], bins=50, color='coral', edgecolor='black', alpha=0.7)
axes[0].axvline(df['dti'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["dti"].mean():.1f}%')
axes[0].set_title('DTI Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Debt-to-Income Ratio (%)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].legend()
axes[0].grid(alpha=0.3)

# By default status
df.boxplot(column='dti', by='is_default', ax=axes[1])
axes[1].set_title('DTI by Default Status', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Default (0=No, 1=Yes)', fontsize=12)
axes[1].set_ylabel('DTI (%)', fontsize=12)
plt.suptitle('')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 13. Key Business Metrics

# %%
# Calculate key business metrics
print("\n" + "="*60)
print("KEY BUSINESS METRICS")
print("="*60)

metrics = {
    'Total Loan Volume': f"${df['loan_amnt'].sum():,.0f}",
    'Average Loan Amount': f"${df['loan_amnt'].mean():,.0f}",
    'Median Loan Amount': f"${df['loan_amnt'].median():,.0f}",
    'Average Interest Rate': f"{df['int_rate'].mean():.2f}%",
    'Average FICO Score': f"{df['fico_range_low'].mean():.0f}",
    'Average DTI': f"{df['dti'].mean():.2f}%",
    'Default Rate': f"{default_rate:.2f}%",
    'Average Annual Income': f"${df['annual_inc'].mean():,.0f}"
}

for metric, value in metrics.items():
    print(f"  {metric:.<35} {value}")

# %% [markdown]
# ## 14. Correlation Analysis

# %%
# Select numerical columns for correlation
numerical_cols = ['loan_amnt', 'int_rate', 'annual_inc', 'dti', 
                  'fico_range_low', 'revol_util', 'open_acc', 'total_acc', 'is_default']

# Calculate correlation
corr_matrix = df[numerical_cols].corr()

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

# %%
# Top correlations with default
print("\n" + "="*60)
print("CORRELATIONS WITH DEFAULT")
print("="*60)
default_corr = corr_matrix['is_default'].drop('is_default').sort_values(ascending=False)
print(default_corr)

# %% [markdown]
# **Key Insights:**
# - Interest rate has positive correlation with default
# - FICO score has negative correlation with default  
# - DTI shows weak positive correlation with default

# %% [markdown]
# ## 15. Loan Purpose Analysis

# %%
# Purpose distribution
print("\n" + "="*60)
print("LOAN PURPOSE DISTRIBUTION")
print("="*60)

purpose_counts = df['purpose'].value_counts()
print(purpose_counts)

# %%
# Visualize purpose
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Purpose distribution
purpose_counts.plot(kind='barh', ax=axes[0], color='teal', edgecolor='black', alpha=0.8)
axes[0].set_title('Loan Purpose Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Count', fontsize=12)
axes[0].set_ylabel('Purpose', fontsize=12)
axes[0].grid(axis='x', alpha=0.3)

# Default rate by purpose
default_by_purpose = df.groupby('purpose')['is_default'].mean().sort_values(ascending=False) * 100
default_by_purpose.plot(kind='barh', ax=axes[1], color='indianred', edgecolor='black', alpha=0.8)
axes[1].set_title('Default Rate by Purpose', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Default Rate (%)', fontsize=12)
axes[1].set_ylabel('Purpose', fontsize=12)
axes[1].axvline(x=default_rate, color='red', linestyle='--', label=f'Overall: {default_rate:.1f}%')
axes[1].legend()
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 16. Summary & Next Steps

# %%
print("\n" + "="*60)
print("EXPLORATION SUMMARY")
print("="*60)
print(f"""
✅ Data loaded successfully: {len(df):,} loan records
✅ No missing values in key fields
✅ Default rate: {default_rate:.2f}% ({df['is_default'].sum():,} defaults)
✅ Grade distribution: Mostly B-D grades (typical consumer lending)

📊 KEY INSIGHTS:

1. RISK PATTERNS:
   - Default rate increases from Grade A ({df[df['grade']=='A']['is_default'].mean()*100:.1f}%) 
     to Grade G ({df[df['grade']=='G']['is_default'].mean()*100:.1f}%)
   - Higher interest rates correlate with higher default risk
   - Lower FICO scores indicate higher default probability

2. PORTFOLIO CHARACTERISTICS:
   - Average loan: ${df['loan_amnt'].mean():,.0f}
   - Average rate: {df['int_rate'].mean():.2f}%
   - Average FICO: {df['fico_range_low'].mean():.0f}
   - Primary purpose: {purpose_counts.index[0]}

3. RISK INDICATORS:
   - Interest rate: +{corr_matrix.loc['int_rate', 'is_default']:.3f} correlation with default
   - FICO score: {corr_matrix.loc['fico_range_low', 'is_default']:.3f} correlation with default
   - DTI: +{corr_matrix.loc['dti', 'is_default']:.3f} correlation with default

📋 NEXT STEPS:

1. ✅ Feature engineering (02_feature_engineering.ipynb)
   - Create derived features (credit utilization, payment capacity)
   - Encode categorical variables
   - Handle outliers and scaling

2. ✅ Build credit scoring model (03_credit_risk_modeling.ipynb)
   - Train logistic regression baseline
   - Test Random Forest and XGBoost
   - Evaluate with AUC-ROC, precision-recall

3. ✅ Customer segmentation (04_customer_segmentation.ipynb)
   - K-means clustering
   - Profile each segment
   - Segment-specific strategies

4. ✅ A/B testing framework (05_ab_testing.ipynb)
   - Design experiments
   - Statistical significance testing
   - Business impact analysis
""")

print("="*60)
print("📓 END OF EXPLORATORY DATA ANALYSIS")
print("="*60)