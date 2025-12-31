-- ============================================================================
-- Dashboard KPI Views
-- ============================================================================
-- Purpose: Materialized views for BI dashboards and reporting
-- Business Use: Executive dashboards, KPI monitoring, real-time analytics
-- ============================================================================

-- ============================================================================
-- View 1: Executive Summary Dashboard
-- ============================================================================

CREATE OR REPLACE VIEW vw_executive_summary AS
SELECT 
    -- Portfolio size
    COUNT(DISTINCT f.loan_id) AS total_loans,
    COUNT(DISTINCT f.customer_id) AS total_customers,
    ROUND(SUM(f.loan_amount), 2) AS total_loan_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    
    -- Risk metrics
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS npl_ratio_pct,
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    
    -- Revenue metrics
    ROUND(SUM(f.total_interest_received), 2) AS total_interest_income,
    ROUND(SUM(f.total_payment), 2) AS total_payments_received,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    
    -- Profitability
    ROUND(SUM(f.net_profit_loss), 2) AS total_net_profit,
    ROUND(100.0 * SUM(f.net_profit_loss) / NULLIF(SUM(f.funded_amount), 0), 2) AS portfolio_roi_pct,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id;

-- ============================================================================
-- View 2: Risk Monitoring Dashboard
-- ============================================================================

CREATE OR REPLACE VIEW vw_risk_monitoring AS
SELECT 
    p.loan_grade,
    c.risk_category,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS volume_pct,
    
    -- Default metrics
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    -- Risk indicators
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    ROUND(AVG(c.dti_ratio), 2) AS avg_dti_ratio,
    ROUND(AVG(c.credit_utilization), 2) AS avg_credit_utilization,
    
    -- Pricing
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_products p ON f.product_id = p.product_id
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY p.loan_grade, c.risk_category

ORDER BY p.loan_grade, c.risk_category;

-- ============================================================================
-- View 3: Monthly Performance Trends
-- ============================================================================

CREATE OR REPLACE VIEW vw_monthly_trends AS
SELECT 
    t.year,
    t.month,
    t.month_name,
    t.quarter,
    
    -- Volume metrics
    COUNT(DISTINCT f.loan_id) AS loans_originated,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    
    -- Customer metrics
    COUNT(DISTINCT f.customer_id) AS unique_customers,
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    ROUND(AVG(c.annual_income), 2) AS avg_annual_income,
    
    -- Risk metrics
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    -- Revenue metrics
    ROUND(SUM(f.total_interest_received), 2) AS interest_income,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    
    -- Profitability
    ROUND(SUM(f.net_profit_loss), 2) AS net_profit,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_time t ON f.issue_date_id = t.date_id
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY t.year, t.month, t.month_name, t.quarter

ORDER BY t.year DESC, t.month DESC;

-- ============================================================================
-- View 4: Customer Segment Performance
-- ============================================================================

CREATE OR REPLACE VIEW vw_segment_performance AS
SELECT 
    c.customer_segment,
    c.risk_category,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    COUNT(DISTINCT f.customer_id) AS total_customers,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    
    -- Customer profile
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    ROUND(AVG(c.annual_income), 2) AS avg_annual_income,
    ROUND(AVG(c.dti_ratio), 2) AS avg_dti_ratio,
    ROUND(AVG(c.credit_utilization), 2) AS avg_credit_utilization,
    ROUND(AVG(c.employment_length), 1) AS avg_employment_years,
    
    -- Performance
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    SUM(CASE WHEN f.loan_status = 'Fully Paid' THEN 1 ELSE 0 END) AS paid_off_count,
    ROUND(100.0 * SUM(CASE WHEN f.loan_status = 'Fully Paid' THEN 1 ELSE 0 END) / COUNT(*), 2) AS payoff_rate_pct,
    
    -- Revenue
    ROUND(SUM(f.total_interest_received), 2) AS total_interest_income,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    
    -- Profitability
    ROUND(SUM(f.net_profit_loss), 2) AS total_net_profit,
    ROUND(AVG(f.net_profit_loss), 2) AS avg_net_profit_per_loan,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY c.customer_segment, c.risk_category

ORDER BY total_volume DESC;

-- ============================================================================
-- View 5: Geographic Performance
-- ============================================================================

CREATE OR REPLACE VIEW vw_geographic_performance AS
SELECT 
    g.region,
    g.state_code,
    g.state_name,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    
    -- Customer profile
    ROUND(AVG(c.fico_score), 0) AS avg_fico_score,
    ROUND(AVG(c.annual_income), 2) AS avg_annual_income,
    
    -- Performance
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    -- Revenue
    ROUND(SUM(f.total_interest_received), 2) AS interest_income,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_geography g ON f.geography_id = g.geography_id
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY g.region, g.state_code, g.state_name

HAVING COUNT(DISTINCT f.loan_id) >= 50  -- Minimum sample size

ORDER BY total_volume DESC;

-- ============================================================================
-- View 6: Cohort Analysis Dashboard
-- ============================================================================

CREATE OR REPLACE VIEW vw_cohort_analysis AS
SELECT 
    t.vintage_month AS cohort,
    t.year AS cohort_year,
    t.quarter AS cohort_quarter,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    
    -- Performance
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    SUM(CASE WHEN f.loan_status = 'Fully Paid' THEN 1 ELSE 0 END) AS paid_off,
    ROUND(100.0 * SUM(CASE WHEN f.loan_status = 'Fully Paid' THEN 1 ELSE 0 END) / COUNT(*), 2) AS payoff_rate_pct,
    
    SUM(CASE WHEN f.is_current = TRUE THEN 1 ELSE 0 END) AS current_loans,
    ROUND(100.0 * SUM(CASE WHEN f.is_current = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS current_rate_pct,
    
    -- Financial
    ROUND(SUM(f.total_payment), 2) AS total_payments,
    ROUND(SUM(f.total_interest_received), 2) AS total_interest,
    ROUND(SUM(f.net_profit_loss), 2) AS net_profit,
    
    -- Maturity
    ROUND(AVG(f.months_since_issue), 1) AS avg_months_since_issue,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_time t ON f.issue_date_id = t.date_id

GROUP BY t.vintage_month, t.year, t.quarter

ORDER BY t.year DESC, t.quarter DESC;

-- ============================================================================
-- View 7: Product Performance
-- ============================================================================

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT 
    p.loan_grade,
    p.loan_sub_grade,
    p.loan_term,
    p.loan_purpose,
    
    -- Volume
    COUNT(DISTINCT f.loan_id) AS total_loans,
    ROUND(SUM(f.loan_amount), 2) AS total_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    
    -- Risk
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score,
    
    -- Performance
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    -- Pricing
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    ROUND(AVG(f.installment), 2) AS avg_installment,
    
    -- Revenue
    ROUND(SUM(f.total_interest_received), 2) AS total_interest_income,
    ROUND(SUM(f.net_profit_loss), 2) AS total_net_profit,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_products p ON f.product_id = p.product_id

GROUP BY p.loan_grade, p.loan_sub_grade, p.loan_term, p.loan_purpose

ORDER BY total_volume DESC;

-- ============================================================================
-- View 8: High-Risk Portfolio Alert
-- ============================================================================

CREATE OR REPLACE VIEW vw_high_risk_alerts AS
SELECT 
    f.loan_id,
    f.customer_id,
    c.customer_segment,
    c.risk_category,
    
    -- Loan details
    f.loan_amount,
    f.loan_status,
    p.loan_grade,
    f.interest_rate,
    
    -- Risk indicators
    f.risk_score,
    f.predicted_default_probability,
    c.fico_score,
    c.dti_ratio,
    c.credit_utilization,
    c.delinquencies_2yrs,
    
    -- Time
    f.months_since_issue,
    f.last_payment_date,
    
    -- Priority score
    ROUND(
        (f.risk_score * 0.4) + 
        (c.credit_utilization * 0.3) + 
        (c.dti_ratio * 0.3),
    2) AS priority_score,
    
    -- Alert level
    CASE 
        WHEN f.risk_score > 85 OR c.credit_utilization > 90 THEN 'CRITICAL'
        WHEN f.risk_score > 75 OR c.credit_utilization > 80 THEN 'HIGH'
        WHEN f.risk_score > 65 OR c.credit_utilization > 70 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS alert_level,
    
    -- Current timestamp
    CURRENT_TIMESTAMP AS last_updated

FROM fact_loans f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id
INNER JOIN dim_products p ON f.product_id = p.product_id

WHERE 
    f.is_current = TRUE
    AND (
        f.risk_score > 65
        OR c.credit_utilization > 70
        OR c.dti_ratio > 35
        OR c.delinquencies_2yrs > 0
    )

ORDER BY priority_score DESC, f.loan_amount DESC;

-- ============================================================================
-- Usage Examples
-- ============================================================================

-- Example 1: Query executive summary
-- SELECT * FROM vw_executive_summary;

-- Example 2: Monitor risk by grade
-- SELECT * FROM vw_risk_monitoring ORDER BY default_rate_pct DESC;

-- Example 3: Track monthly trends
-- SELECT * FROM vw_monthly_trends WHERE year >= 2017 ORDER BY year DESC, month DESC;

-- Example 4: Analyze segment performance
-- SELECT * FROM vw_segment_performance ORDER BY default_rate_pct DESC;

-- Example 5: Geographic analysis
-- SELECT * FROM vw_geographic_performance ORDER BY default_rate_pct DESC LIMIT 10;

-- Example 6: Cohort performance
-- SELECT * FROM vw_cohort_analysis WHERE cohort_year >= 2017 ORDER BY cohort_year DESC;

-- Example 7: Product analysis
-- SELECT * FROM vw_product_performance WHERE loan_purpose = 'debt_consolidation';

-- Example 8: High-risk alerts
-- SELECT * FROM vw_high_risk_alerts WHERE alert_level IN ('CRITICAL', 'HIGH') LIMIT 50;
