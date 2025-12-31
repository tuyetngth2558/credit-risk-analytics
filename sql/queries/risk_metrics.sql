-- ============================================================================
-- Risk Metrics and Portfolio Health
-- ============================================================================
-- Purpose: Calculate key risk metrics for portfolio monitoring
-- Business Use: Executive dashboard KPIs and risk monitoring
-- ============================================================================

-- ============================================================================
-- 1. Portfolio Overview Metrics
-- ============================================================================

WITH portfolio_summary AS (
    SELECT 
        COUNT(DISTINCT loan_id) AS total_loans,
        COUNT(DISTINCT customer_id) AS total_customers,
        SUM(loan_amount) AS total_loan_volume,
        SUM(funded_amount) AS total_funded_amount,
        
        -- Default metrics
        SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) AS total_defaults,
        SUM(CASE WHEN is_default = TRUE THEN loan_amount ELSE 0 END) AS default_volume,
        
        -- Current portfolio
        SUM(CASE WHEN is_current = TRUE THEN loan_amount ELSE 0 END) AS current_portfolio_value,
        
        -- Revenue metrics
        SUM(total_interest_received) AS total_interest_income,
        SUM(total_payment) AS total_payments_received,
        SUM(net_profit_loss) AS total_net_profit_loss
        
    FROM fact_loans
)

SELECT 
    total_loans,
    total_customers,
    ROUND(total_loan_volume, 2) AS total_loan_volume,
    ROUND(total_funded_amount, 2) AS total_funded_amount,
    
    -- NPL (Non-Performing Loan) Ratio
    total_defaults,
    ROUND(100.0 * total_defaults / NULLIF(total_loans, 0), 2) AS npl_ratio_pct,
    ROUND(default_volume, 2) AS default_volume,
    ROUND(100.0 * default_volume / NULLIF(total_loan_volume, 0), 2) AS npl_volume_pct,
    
    -- Portfolio health
    ROUND(current_portfolio_value, 2) AS current_portfolio_value,
    
    -- Profitability
    ROUND(total_interest_income, 2) AS total_interest_income,
    ROUND(total_payments_received, 2) AS total_payments_received,
    ROUND(total_net_profit_loss, 2) AS total_net_profit_loss,
    ROUND(100.0 * total_net_profit_loss / NULLIF(total_funded_amount, 0), 2) AS portfolio_roi_pct

FROM portfolio_summary;

-- ============================================================================
-- 2. Risk Metrics by Grade
-- ============================================================================

SELECT 
    p.loan_grade,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    
    -- Risk metrics
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    ROUND(AVG(c.dti_ratio), 2) AS avg_dti_ratio,
    ROUND(AVG(c.credit_utilization), 2) AS avg_credit_utilization,
    
    -- Performance
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    -- Pricing
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    
    -- Profitability
    ROUND(SUM(f.total_interest_received), 2) AS total_interest_income,
    ROUND(AVG(f.net_profit_loss), 2) AS avg_net_profit_loss

FROM fact_loans f
INNER JOIN dim_products p ON f.product_id = p.product_id
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY p.loan_grade

ORDER BY p.loan_grade;

-- ============================================================================
-- 3. Monthly Trend Analysis
-- ============================================================================

SELECT 
    t.year,
    t.month,
    t.month_name,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS loans_originated,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    
    -- Risk
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    
    -- Performance (for mature loans)
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS default_rate_pct,
    
    -- Revenue
    ROUND(SUM(f.total_interest_received), 2) AS interest_income

FROM fact_loans f
INNER JOIN dim_time t ON f.issue_date_id = t.date_id
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

WHERE t.year >= 2016

GROUP BY t.year, t.month, t.month_name

ORDER BY t.year DESC, t.month DESC

LIMIT 24;  -- Last 24 months

-- ============================================================================
-- 4. Geographic Risk Distribution
-- ============================================================================

SELECT 
    g.state_code,
    g.state_name,
    g.region,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    
    -- Risk
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    
    -- Performance
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    -- Customer profile
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    ROUND(AVG(c.annual_income), 2) AS avg_annual_income

FROM fact_loans f
INNER JOIN dim_geography g ON f.geography_id = g.geography_id
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY g.state_code, g.state_name, g.region

HAVING COUNT(DISTINCT f.loan_id) >= 100  -- Minimum sample size

ORDER BY default_rate_pct DESC

LIMIT 20;

-- ============================================================================
-- 5. Early Warning Indicators
-- ============================================================================
-- Identify high-risk loans requiring attention

SELECT 
    f.loan_id,
    f.customer_id,
    c.customer_segment,
    f.loan_amount,
    f.loan_status,
    
    -- Risk indicators
    f.risk_score,
    f.predicted_default_probability,
    c.fico_score,
    c.dti_ratio,
    c.credit_utilization,
    c.delinquencies_2yrs,
    
    -- Loan details
    p.loan_grade,
    f.interest_rate,
    f.months_since_issue,
    f.last_payment_date,
    
    -- Priority score (higher = more urgent)
    ROUND(
        (f.risk_score * 0.4) + 
        (c.credit_utilization * 0.3) + 
        (c.dti_ratio * 0.3),
    2) AS priority_score

FROM fact_loans f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id
INNER JOIN dim_products p ON f.product_id = p.product_id

WHERE 
    f.is_current = TRUE  -- Active loans only
    AND (
        f.risk_score > 75  -- High risk score
        OR c.credit_utilization > 80  -- High utilization
        OR c.dti_ratio > 40  -- High DTI
        OR c.delinquencies_2yrs > 0  -- Recent delinquencies
    )

ORDER BY priority_score DESC, f.loan_amount DESC

LIMIT 100;  -- Top 100 high-risk loans
