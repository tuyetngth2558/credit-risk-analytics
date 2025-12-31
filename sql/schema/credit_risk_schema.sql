-- ============================================================================
-- Credit Risk Analytics - Database Schema
-- ============================================================================
-- Star Schema Design for Credit Risk Analytics
-- Optimized for analytical queries and BI dashboards
-- ============================================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS fact_loans CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_time CASCADE;
DROP TABLE IF EXISTS dim_geography CASCADE;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- Dimension: Customers
-- Contains customer demographic and credit profile information
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    fico_score INTEGER,
    fico_category VARCHAR(50),
    annual_income DECIMAL(12, 2),
    employment_length INTEGER,
    employment_stability VARCHAR(50),
    home_ownership VARCHAR(50),
    verification_status VARCHAR(50),
    
    -- Credit history
    delinquencies_2yrs INTEGER,
    inquiries_last_6mths INTEGER,
    open_accounts INTEGER,
    public_records INTEGER,
    revolving_balance DECIMAL(12, 2),
    revolving_utilization DECIMAL(5, 2),
    total_accounts INTEGER,
    
    -- Derived features
    credit_utilization DECIMAL(5, 2),
    dti_ratio DECIMAL(5, 2),
    dti_bucket VARCHAR(50),
    
    -- Segmentation
    customer_segment VARCHAR(50),
    risk_category VARCHAR(50),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Products
-- Contains loan product characteristics
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    loan_grade VARCHAR(10),
    loan_sub_grade VARCHAR(10),
    loan_term INTEGER,
    loan_purpose VARCHAR(100),
    
    -- Product categorization
    product_category VARCHAR(50),
    risk_tier VARCHAR(50),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Time
-- Time dimension for temporal analysis
CREATE TABLE dim_time (
    date_id INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    week INTEGER,
    day_of_month INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(20),
    
    -- Business calendar
    is_weekend BOOLEAN,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    
    -- Vintage cohort
    vintage_month VARCHAR(20)
);

-- Dimension: Geography
-- Geographic information for regional analysis
CREATE TABLE dim_geography (
    geography_id VARCHAR(50) PRIMARY KEY,
    state_code VARCHAR(2),
    state_name VARCHAR(100),
    region VARCHAR(50),
    zip_code VARCHAR(10),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- FACT TABLE
-- ============================================================================

-- Fact: Loans
-- Central fact table containing loan transactions and outcomes
CREATE TABLE fact_loans (
    loan_id VARCHAR(50) PRIMARY KEY,
    
    -- Foreign keys to dimensions
    customer_id VARCHAR(50) REFERENCES dim_customers(customer_id),
    product_id VARCHAR(50) REFERENCES dim_products(product_id),
    issue_date_id INTEGER REFERENCES dim_time(date_id),
    geography_id VARCHAR(50) REFERENCES dim_geography(geography_id),
    
    -- Loan details
    loan_amount DECIMAL(12, 2),
    funded_amount DECIMAL(12, 2),
    interest_rate DECIMAL(5, 2),
    installment DECIMAL(10, 2),
    
    -- Loan status
    loan_status VARCHAR(50),
    is_default BOOLEAN,
    is_current BOOLEAN,
    is_paid_off BOOLEAN,
    
    -- Payment information
    total_payment DECIMAL(12, 2),
    total_principal_received DECIMAL(12, 2),
    total_interest_received DECIMAL(12, 2),
    last_payment_amount DECIMAL(10, 2),
    last_payment_date DATE,
    
    -- Risk metrics
    risk_score DECIMAL(5, 2),
    predicted_default_probability DECIMAL(5, 4),
    
    -- Derived metrics
    loan_to_income_ratio DECIMAL(5, 2),
    months_since_issue INTEGER,
    
    -- Financial metrics
    net_profit_loss DECIMAL(12, 2),
    roi DECIMAL(5, 2),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Fact table indexes
CREATE INDEX idx_fact_loans_customer ON fact_loans(customer_id);
CREATE INDEX idx_fact_loans_product ON fact_loans(product_id);
CREATE INDEX idx_fact_loans_issue_date ON fact_loans(issue_date_id);
CREATE INDEX idx_fact_loans_geography ON fact_loans(geography_id);
CREATE INDEX idx_fact_loans_status ON fact_loans(loan_status);
CREATE INDEX idx_fact_loans_default ON fact_loans(is_default);

-- Dimension table indexes
CREATE INDEX idx_dim_customers_segment ON dim_customers(customer_segment);
CREATE INDEX idx_dim_customers_risk ON dim_customers(risk_category);
CREATE INDEX idx_dim_customers_fico ON dim_customers(fico_score);
CREATE INDEX idx_dim_products_grade ON dim_products(loan_grade);
CREATE INDEX idx_dim_time_year_month ON dim_time(year, month);
CREATE INDEX idx_dim_geography_state ON dim_geography(state_code);

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE fact_loans IS 'Central fact table containing loan transactions and outcomes';
COMMENT ON TABLE dim_customers IS 'Customer dimension with demographic and credit profile';
COMMENT ON TABLE dim_products IS 'Product dimension with loan characteristics';
COMMENT ON TABLE dim_time IS 'Time dimension for temporal analysis';
COMMENT ON TABLE dim_geography IS 'Geography dimension for regional analysis';

-- ============================================================================
-- SAMPLE DATA VALIDATION QUERIES
-- ============================================================================

-- Verify table creation
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Check row counts
-- SELECT 'fact_loans' as table_name, COUNT(*) as row_count FROM fact_loans
-- UNION ALL
-- SELECT 'dim_customers', COUNT(*) FROM dim_customers
-- UNION ALL
-- SELECT 'dim_products', COUNT(*) FROM dim_products
-- UNION ALL
-- SELECT 'dim_time', COUNT(*) FROM dim_time
-- UNION ALL
-- SELECT 'dim_geography', COUNT(*) FROM dim_geography;
