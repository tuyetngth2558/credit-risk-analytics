"""
Configuration management for Credit Risk Analytics project
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

# ==================== PROJECT PATHS ====================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_PATH / "raw"
INTERIM_DATA_PATH = DATA_PATH / "interim"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
SAMPLE_DATA_PATH = DATA_PATH / "sample"
EXTERNAL_DATA_PATH = DATA_PATH / "external"

# Create directories if they don't exist
for path in [RAW_DATA_PATH, INTERIM_DATA_PATH, PROCESSED_DATA_PATH, 
             SAMPLE_DATA_PATH, EXTERNAL_DATA_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# ==================== DATABASE CONFIG ====================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "credit_risk_db"),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", "")
}

# ==================== SNOWFLAKE CONFIG ====================
SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "database": os.getenv("SNOWFLAKE_DATABASE", "CREDIT_RISK_DB"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA", "ANALYTICS"),
    "role": os.getenv("SNOWFLAKE_ROLE", "ANALYST")
}

# ==================== KAGGLE CONFIG ====================
KAGGLE_CONFIG = {
    "username": os.getenv("KAGGLE_USERNAME"),
    "key": os.getenv("KAGGLE_KEY")
}

# ==================== LOGGING CONFIG ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== MODEL PARAMETERS ====================
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))
TEST_SIZE = float(os.getenv("TEST_SIZE", "0.2"))
VALIDATION_SIZE = 0.2
N_FOLDS = 5  # For cross-validation

# ==================== DATA PROCESSING PARAMETERS ====================
# Column names for key features
NUMERICAL_FEATURES = [
    'loan_amnt', 'funded_amnt', 'int_rate', 'installment', 
    'annual_inc', 'dti', 'open_acc', 'pub_rec', 'revol_bal', 
    'revol_util', 'total_acc', 'fico_range_low', 'fico_range_high'
]

CATEGORICAL_FEATURES = [
    'term', 'grade', 'sub_grade', 'emp_length', 'home_ownership',
    'verification_status', 'purpose', 'initial_list_status'
]

TARGET_COLUMN = 'loan_status'

# Define what constitutes a "default"
DEFAULT_STATUSES = ['Charged Off', 'Default', 'Late (31-120 days)']
GOOD_STATUSES = ['Fully Paid', 'Current']

# ==================== FEATURE ENGINEERING ====================
# Credit score bins
FICO_BINS = [300, 580, 620, 660, 700, 740, 780, 850]
FICO_LABELS = ['Very Poor', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent', 'Exceptional']

# DTI bins
DTI_BINS = [0, 10, 20, 30, 40, 100]
DTI_LABELS = ['Very Low', 'Low', 'Medium', 'High', 'Very High']

# Income bins
INCOME_BINS = [0, 40000, 60000, 80000, 120000, 500000]
INCOME_LABELS = ['Low', 'Lower Middle', 'Middle', 'Upper Middle', 'High']

# ==================== MODEL CONFIGURATION ====================
MODEL_PARAMS = {
    'logistic_regression': {
        'max_iter': 1000,
        'random_state': RANDOM_SEED,
        'class_weight': 'balanced',
        'solver': 'liblinear'
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 20,
        'min_samples_leaf': 10,
        'random_state': RANDOM_SEED,
        'class_weight': 'balanced',
        'n_jobs': -1
    },
    'xgboost': {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': RANDOM_SEED
    }
}

# ==================== EVALUATION METRICS ====================
CLASSIFICATION_THRESHOLD = 0.5
METRICS_TO_TRACK = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

# ==================== DASHBOARD CONFIG ====================
DASHBOARD_REFRESH_RATE = 3600  # seconds (1 hour)
ALERT_THRESHOLDS = {
    'default_rate': 0.05,  # 5%
    'approval_rate': 0.30,  # 30%
    'avg_loan_amount': 20000
}

# ==================== SAMPLE DATA CONFIG ====================
SAMPLE_SIZE = 10000  # Number of records for sample data
SAMPLE_RANDOM_STATE = RANDOM_SEED

# ==================== UTILITY FUNCTIONS ====================
def get_data_path(filename, data_type='raw'):
    """
    Get full path to data file
    
    Args:
        filename: Name of the file
        data_type: Type of data ('raw', 'processed', 'sample', etc.)
    
    Returns:
        Path object to the file
    """
    data_type_map = {
        'raw': RAW_DATA_PATH,
        'interim': INTERIM_DATA_PATH,
        'processed': PROCESSED_DATA_PATH,
        'sample': SAMPLE_DATA_PATH,
        'external': EXTERNAL_DATA_PATH
    }
    
    base_path = data_type_map.get(data_type, RAW_DATA_PATH)
    return base_path / filename

def print_config():
    """Print current configuration"""
    print("="*60)
    print("CREDIT RISK ANALYTICS - CONFIGURATION")
    print("="*60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Path: {DATA_PATH}")
    print(f"Random Seed: {RANDOM_SEED}")
    print(f"Test Size: {TEST_SIZE}")
    print(f"Log Level: {LOG_LEVEL}")
    print("="*60)

if __name__ == "__main__":
    print_config()
    print("\n✓ Configuration loaded successfully!")
    print(f"✓ All data directories created")