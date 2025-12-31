"""
Create sample dashboard previews for portfolio showcase
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import SAMPLE_DATA_PATH

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def create_risk_monitoring_dashboard():
    """Create Executive Risk Monitoring Dashboard"""
    
    # Load data
    df = pd.read_csv(SAMPLE_DATA_PATH / 'sample_loans_10k.csv')
    default_statuses = ['Charged Off', 'Default', 'Late (31-120 days)']
    df['is_default'] = df['loan_status'].isin(default_statuses).astype(int)
    
    # Create figure
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('white')
    
    # Title
    fig.text(0.5, 0.96, 'Executive Risk Monitoring Dashboard', 
             ha='center', fontsize=22, fontweight='bold')
    
    # Calculate KPIs
    default_rate = df['is_default'].mean() * 100
    avg_loan = df['loan_amnt'].mean()
    total_volume = df['loan_amnt'].sum()
    avg_fico = df['fico_range_low'].mean()
    
    # KPI Cards
    kpi_y = 0.88
    fig.text(0.15, kpi_y, f'Portfolio NPL\n{default_rate:.2f}%', 
             ha='center', fontsize=14, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#ffcccc', edgecolor='red', linewidth=2))
    
    fig.text(0.35, kpi_y, f'Total Volume\n${total_volume/1e6:.1f}M', 
             ha='center', fontsize=14, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#ccffcc', edgecolor='green', linewidth=2))
    
    fig.text(0.55, kpi_y, f'Avg Loan Amount\n${avg_loan:,.0f}', 
             ha='center', fontsize=14, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#ccccff', edgecolor='blue', linewidth=2))
    
    fig.text(0.75, kpi_y, f'Avg FICO Score\n{avg_fico:.0f}', 
             ha='center', fontsize=14, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='#ffffcc', edgecolor='orange', linewidth=2))
    
    # Chart 1: Default Rate by Grade (Top Left)
    ax1 = plt.subplot(3, 3, 4)
    default_by_grade = df.groupby('grade')['is_default'].mean() * 100
    bars = ax1.bar(default_by_grade.index, default_by_grade.values, 
                   color='salmon', edgecolor='darkred', linewidth=1.5)
    ax1.axhline(y=default_rate, color='red', linestyle='--', linewidth=2, label=f'Portfolio Avg: {default_rate:.1f}%')
    ax1.set_title('Default Rate by Risk Grade', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Grade', fontsize=10)
    ax1.set_ylabel('Default Rate (%)', fontsize=10)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Chart 2: Loan Status Distribution (Top Middle)
    ax2 = plt.subplot(3, 3, 5)
    status_counts = df['loan_status'].value_counts()
    colors_pie = ['#66b3ff', '#99ff99', '#ff9999', '#ffcc99', '#ff99cc']
    wedges, texts, autotexts = ax2.pie(status_counts.values, labels=status_counts.index, 
                                        autopct='%1.1f%%', colors=colors_pie, 
                                        startangle=90, textprops={'fontsize': 9})
    ax2.set_title('Loan Status Distribution', fontsize=12, fontweight='bold')
    
    # Chart 3: Risk Score Distribution (Top Right)
    ax3 = plt.subplot(3, 3, 6)
    ax3.hist(df['fico_range_low'], bins=30, color='purple', alpha=0.7, edgecolor='black')
    ax3.axvline(x=avg_fico, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_fico:.0f}')
    ax3.set_title('FICO Score Distribution', fontsize=12, fontweight='bold')
    ax3.set_xlabel('FICO Score', fontsize=10)
    ax3.set_ylabel('Frequency', fontsize=10)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Chart 4: Loan Amount by Grade (Middle Left)
    ax4 = plt.subplot(3, 3, 7)
    df.boxplot(column='loan_amnt', by='grade', ax=ax4)
    ax4.set_title('Loan Amount Distribution by Grade', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Grade', fontsize=10)
    ax4.set_ylabel('Loan Amount ($)', fontsize=10)
    plt.suptitle('')
    
    # Chart 5: Interest Rate Trend (Middle Middle)
    ax5 = plt.subplot(3, 3, 8)
    avg_rate_by_grade = df.groupby('grade')['int_rate'].mean()
    ax5.plot(avg_rate_by_grade.index, avg_rate_by_grade.values, 
             marker='o', linewidth=2, markersize=8, color='orange')
    ax5.fill_between(range(len(avg_rate_by_grade)), avg_rate_by_grade.values, alpha=0.3, color='orange')
    ax5.set_title('Average Interest Rate by Grade', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Grade', fontsize=10)
    ax5.set_ylabel('Interest Rate (%)', fontsize=10)
    ax5.grid(alpha=0.3)
    
    # Chart 6: Approval Funnel (Middle Right)
    ax6 = plt.subplot(3, 3, 9)
    funnel_stages = ['Applications', 'Pre-Approved', 'Verified', 'Funded']
    funnel_values = [10000, 7500, 6500, 6000]
    colors_funnel = ['#ff9999', '#ffcc99', '#99ff99', '#66b3ff']
    ax6.barh(funnel_stages, funnel_values, color=colors_funnel, edgecolor='black', linewidth=1.5)
    ax6.set_title('Loan Approval Funnel', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Count', fontsize=10)
    for i, v in enumerate(funnel_values):
        ax6.text(v + 200, i, f'{v:,}', va='center', fontsize=10, fontweight='bold')
    ax6.grid(axis='x', alpha=0.3)
    
    # Chart 7: DTI Distribution (Bottom Left)
    ax7 = plt.subplot(3, 3, 1)
    ax7.hist(df['dti'], bins=30, color='teal', alpha=0.7, edgecolor='black')
    ax7.axvline(x=df['dti'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["dti"].mean():.1f}%')
    ax7.set_title('Debt-to-Income Distribution', fontsize=12, fontweight='bold')
    ax7.set_xlabel('DTI (%)', fontsize=10)
    ax7.set_ylabel('Frequency', fontsize=10)
    ax7.legend()
    ax7.grid(axis='y', alpha=0.3)
    
    # Chart 8: Loan Purpose (Bottom Middle)
    ax8 = plt.subplot(3, 3, 2)
    purpose_counts = df['purpose'].value_counts().head(7)
    ax8.barh(range(len(purpose_counts)), purpose_counts.values, color='lightcoral', edgecolor='black')
    ax8.set_yticks(range(len(purpose_counts)))
    ax8.set_yticklabels(purpose_counts.index, fontsize=9)
    ax8.set_title('Top Loan Purposes', fontsize=12, fontweight='bold')
    ax8.set_xlabel('Count', fontsize=10)
    ax8.grid(axis='x', alpha=0.3)
    
    # Chart 9: Default by Home Ownership (Bottom Right)
    ax9 = plt.subplot(3, 3, 3)
    default_by_home = df.groupby('home_ownership')['is_default'].mean() * 100
    ax9.bar(default_by_home.index, default_by_home.values, color='steelblue', edgecolor='navy', linewidth=1.5)
    ax9.set_title('Default Rate by Home Ownership', fontsize=12, fontweight='bold')
    ax9.set_xlabel('Home Ownership', fontsize=10)
    ax9.set_ylabel('Default Rate (%)', fontsize=10)
    ax9.grid(axis='y', alpha=0.3)
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    # Save
    output_path = Path('dashboards/risk_monitoring.png')
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Created: {output_path}")
    return output_path

def create_cohort_analysis_dashboard():
    """Create Cohort Performance Dashboard"""
    
    # Load data
    df = pd.read_csv(SAMPLE_DATA_PATH / 'sample_loans_10k.csv')
    default_statuses = ['Charged Off', 'Default', 'Late (31-120 days)']
    df['is_default'] = df['loan_status'].isin(default_statuses).astype(int)
    df['issue_date'] = pd.to_datetime(df['issue_d'])
    df['issue_month'] = df['issue_date'].dt.to_period('M')
    
    # Create figure
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('white')
    
    # Title
    fig.text(0.5, 0.96, 'Cohort Performance Analysis Dashboard', 
             ha='center', fontsize=22, fontweight='bold')
    
    # Chart 1: Loan Volume by Cohort
    ax1 = plt.subplot(2, 3, 1)
    cohort_volume = df.groupby('issue_month')['loan_amnt'].sum() / 1e6
    ax1.bar(range(len(cohort_volume)), cohort_volume.values, color='steelblue', edgecolor='navy')
    ax1.set_title('Loan Volume by Vintage (Monthly)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Cohort Month', fontsize=10)
    ax1.set_ylabel('Volume ($M)', fontsize=10)
    ax1.set_xticks(range(0, len(cohort_volume), 3))
    ax1.set_xticklabels([str(cohort_volume.index[i]) for i in range(0, len(cohort_volume), 3)], rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # Chart 2: Default Rate by Cohort
    ax2 = plt.subplot(2, 3, 2)
    cohort_default = df.groupby('issue_month')['is_default'].mean() * 100
    ax2.plot(range(len(cohort_default)), cohort_default.values, marker='o', linewidth=2, color='red', markersize=6)
    ax2.axhline(y=df['is_default'].mean() * 100, color='gray', linestyle='--', linewidth=2, label='Overall Avg')
    ax2.set_title('Default Rate by Vintage', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Cohort Month', fontsize=10)
    ax2.set_ylabel('Default Rate (%)', fontsize=10)
    ax2.set_xticks(range(0, len(cohort_default), 3))
    ax2.set_xticklabels([str(cohort_default.index[i]) for i in range(0, len(cohort_default), 3)], rotation=45)
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # Chart 3: Cumulative Default Curves
    ax3 = plt.subplot(2, 3, 3)
    cohorts = df['issue_month'].unique()[:5]
    for i, cohort in enumerate(cohorts):
        cohort_df = df[df['issue_month'] == cohort]
        default_rate = cohort_df['is_default'].mean() * 100
        # Simulate cumulative curve
        months = np.arange(0, 12)
        cumulative = default_rate * (1 - np.exp(-months/6))
        ax3.plot(months, cumulative, marker='o', label=str(cohort), linewidth=2)
    ax3.set_title('Cumulative Default Curves (Simulated)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Months Since Origination', fontsize=10)
    ax3.set_ylabel('Cumulative Default Rate (%)', fontsize=10)
    ax3.legend(fontsize=8)
    ax3.grid(alpha=0.3)
    
    # Chart 4: Cohort Counts
    ax4 = plt.subplot(2, 3, 4)
    cohort_counts = df.groupby('issue_month').size()
    ax4.bar(range(len(cohort_counts)), cohort_counts.values, color='lightcoral', edgecolor='darkred')
    ax4.set_title('Loan Count by Cohort', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Cohort Month', fontsize=10)
    ax4.set_ylabel('Loan Count', fontsize=10)
    ax4.set_xticks(range(0, len(cohort_counts), 3))
    ax4.set_xticklabels([str(cohort_counts.index[i]) for i in range(0, len(cohort_counts), 3)], rotation=45)
    ax4.grid(axis='y', alpha=0.3)
    
    # Chart 5: Average Loan Amount Trend
    ax5 = plt.subplot(2, 3, 5)
    cohort_avg_loan = df.groupby('issue_month')['loan_amnt'].mean()
    ax5.plot(range(len(cohort_avg_loan)), cohort_avg_loan.values, marker='s', linewidth=2, color='green', markersize=6)
    ax5.fill_between(range(len(cohort_avg_loan)), cohort_avg_loan.values, alpha=0.3, color='green')
    ax5.set_title('Average Loan Amount Trend', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Cohort Month', fontsize=10)
    ax5.set_ylabel('Avg Loan Amount ($)', fontsize=10)
    ax5.set_xticks(range(0, len(cohort_avg_loan), 3))
    ax5.set_xticklabels([str(cohort_avg_loan.index[i]) for i in range(0, len(cohort_avg_loan), 3)], rotation=45)
    ax5.grid(alpha=0.3)
    
    # Chart 6: Portfolio Aging
    ax6 = plt.subplot(2, 3, 6)
    status_by_cohort = df.groupby(['issue_month', 'loan_status']).size().unstack(fill_value=0)
    status_by_cohort_pct = status_by_cohort.div(status_by_cohort.sum(axis=1), axis=0) * 100
    
    # Select top 3 statuses
    top_statuses = df['loan_status'].value_counts().head(3).index
    bottom = np.zeros(len(status_by_cohort_pct))
    
    for status in top_statuses:
        if status in status_by_cohort_pct.columns:
            ax6.bar(range(len(status_by_cohort_pct)), status_by_cohort_pct[status].values, 
                   bottom=bottom, label=status, edgecolor='black', linewidth=0.5)
            bottom += status_by_cohort_pct[status].values
    
    ax6.set_title('Loan Status Mix by Cohort', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Cohort Month', fontsize=10)
    ax6.set_ylabel('Percentage (%)', fontsize=10)
    ax6.set_xticks(range(0, len(status_by_cohort_pct), 3))
    ax6.set_xticklabels([str(status_by_cohort_pct.index[i]) for i in range(0, len(status_by_cohort_pct), 3)], rotation=45)
    ax6.legend(fontsize=8, loc='upper left')
    ax6.grid(axis='y', alpha=0.3)
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    # Save
    output_path = Path('dashboards/cohort_analysis.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Created: {output_path}")
    return output_path

if __name__ == "__main__":
    print("\n" + "="*60)
    print("CREATING DASHBOARD PREVIEWS")
    print("="*60)
    
    try:
        # Create dashboards
        risk_path = create_risk_monitoring_dashboard()
        cohort_path = create_cohort_analysis_dashboard()
        
        print("\n" + "="*60)
        print("✓ DASHBOARD CREATION COMPLETE!")
        print("="*60)
        print(f"\nDashboards saved to:")
        print(f"  - {risk_path}")
        print(f"  - {cohort_path}")
        print("\nNext steps:")
        print("  1. git add dashboards/")
        print("  2. git commit -m 'Add dashboard previews'")
        print("  3. git push origin main")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()