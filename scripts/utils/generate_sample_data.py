"""Generate synthetic credit data for testing"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config import SAMPLE_DATA_PATH

def generate_sample_loans(n_records=10000):
    """Generate sample loan data"""
    np.random.seed(42)
    random.seed(42)
    
    print(f"Generating {n_records:,} loan records...")
    
    # Generate dates
    start_date = datetime(2015, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 1460)) for _ in range(n_records)]
    
    data = {
        'id': [f'LOAN_{i:08d}' for i in range(n_records)],
        'member_id': [f'MEM_{i:07d}' for i in range(n_records)],
        'loan_amnt': np.random.randint(1000, 40000, n_records),
        'funded_amnt': np.random.randint(1000, 40000, n_records),
        'term': np.random.choice([' 36 months', ' 60 months'], n_records),
        'int_rate': np.round(np.random.uniform(5, 25, n_records), 2),
        'installment': np.random.uniform(50, 1500, n_records),
        'grade': np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 
                                  n_records, 
                                  p=[0.15, 0.20, 0.25, 0.20, 0.12, 0.06, 0.02]),
        'emp_length': np.random.choice(['< 1 year', '1 year', '2 years', '3 years', 
                                       '5 years', '10+ years'], n_records),
        'home_ownership': np.random.choice(['RENT', 'OWN', 'MORTGAGE'], 
                                          n_records, p=[0.35, 0.15, 0.50]),
        'annual_inc': np.random.randint(30000, 200000, n_records),
        'verification_status': np.random.choice(['Verified', 'Not Verified', 'Source Verified'], n_records),
        'issue_d': dates,
        'loan_status': np.random.choice(['Fully Paid', 'Current', 'Charged Off', 
                                        'Late (31-120 days)', 'Default'], 
                                       n_records,
                                       p=[0.65, 0.20, 0.10, 0.03, 0.02]),
        'purpose': np.random.choice(['debt_consolidation', 'credit_card', 'home_improvement', 
                                    'major_purchase', 'medical', 'car', 'other'], n_records),
        'dti': np.round(np.random.uniform(0, 40, n_records), 2),
        'delinq_2yrs': np.random.randint(0, 5, n_records),
        'fico_range_low': np.random.randint(600, 840, n_records),
        'fico_range_high': np.random.randint(605, 850, n_records),
        'open_acc': np.random.randint(2, 30, n_records),
        'pub_rec': np.random.randint(0, 3, n_records),
        'revol_bal': np.random.randint(0, 50000, n_records),
        'revol_util': np.round(np.random.uniform(0, 100, n_records), 1),
        'total_acc': np.random.randint(5, 50, n_records),
        'total_pymnt': np.random.randint(0, 50000, n_records),
    }
    
    df = pd.DataFrame(data)
    
    # Add realistic correlations
    df.loc[df['grade'].isin(['F', 'G']), 'int_rate'] += 5
    df.loc[df['fico_range_low'] < 650, 'int_rate'] += 3
    df.loc[df['dti'] > 30, 'loan_status'] = np.random.choice(
        ['Fully Paid', 'Charged Off', 'Late (31-120 days)'],
        len(df[df['dti'] > 30]),
        p=[0.5, 0.4, 0.1]
    )
    df['fico_range_high'] = df['fico_range_low'] + 5
    
    return df

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GENERATING SAMPLE CREDIT DATA")
    print("="*60)
    
    # Generate data
    df = generate_sample_loans(10000)
    
    # Save to sample folder
    output_path = SAMPLE_DATA_PATH / 'sample_loans_10k.csv'
    df.to_csv(output_path, index=False)
    
    # Statistics
    print(f"\n✓ Generated {len(df):,} records")
    print(f"✓ Saved to: {output_path}")
    print(f"✓ File size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nColumns: {len(df.columns)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\n{'='*60}")
    print("DATA SUMMARY")
    print(f"{'='*60}")
    print("\nLoan Status Distribution:")
    print(df['loan_status'].value_counts())
    print("\nGrade Distribution:")
    print(df['grade'].value_counts().sort_index())
    print("\nSample Records:")
    print(df.head())
    print(f"\n{'='*60}")
    print("✓ SAMPLE DATA GENERATION COMPLETE!")
    print(f"{'='*60}\n")