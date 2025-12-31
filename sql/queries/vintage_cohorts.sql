-- ============================================================================
-- Vintage Cohort Analysis
-- ============================================================================
-- Purpose: Analyze loan performance by origination cohort (vintage)
-- Business Use: Track portfolio aging and identify vintage trends
-- ============================================================================

WITH monthly_cohorts AS (
    SELECT 
        t.vintage_month AS cohort_month,
        t.year AS cohort_year,
        t.quarter AS cohort_quarter,
        f.loan_id,
        f.customer_id,
        f.loan_amount,
        f.loan_status,
        f.is_default,
        f.total_payment,
        f.total_principal_received,
        f.total_interest_received,
        f.months_since_issue,
        p.loan_grade,
        c.customer_segment
        
    FROM fact_loans f
    INNER JOIN dim_time t ON f.issue_date_id = t.date_id
    INNER JOIN dim_products p ON f.product_id = p.product_id
    INNER JOIN dim_customers c ON f.customer_id = c.customer_id
    
    WHERE t.year >= 2015  -- Focus on recent vintages
)

SELECT 
    cohort_month,
    cohort_year,
    cohort_quarter,
    
    -- Volume metrics
    COUNT(DISTINCT loan_id) AS total_loans,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(loan_amount), 2) AS total_loan_volume,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    
    -- Performance metrics
    SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) AS default_count,
    ROUND(100.0 * SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    SUM(CASE WHEN loan_status = 'Fully Paid' THEN 1 ELSE 0 END) AS paid_off_count,
    ROUND(100.0 * SUM(CASE WHEN loan_status = 'Fully Paid' THEN 1 ELSE 0 END) / COUNT(*), 2) AS payoff_rate_pct,
    
    SUM(CASE WHEN loan_status = 'Current' THEN 1 ELSE 0 END) AS current_count,
    ROUND(100.0 * SUM(CASE WHEN loan_status = 'Current' THEN 1 ELSE 0 END) / COUNT(*), 2) AS current_rate_pct,
    
    -- Financial metrics
    ROUND(SUM(total_payment), 2) AS total_payments_received,
    ROUND(SUM(total_principal_received), 2) AS total_principal_received,
    ROUND(SUM(total_interest_received), 2) AS total_interest_received,
    
    -- Maturity
    ROUND(AVG(months_since_issue), 1) AS avg_months_since_issue,
    MAX(months_since_issue) AS max_months_since_issue

FROM monthly_cohorts

GROUP BY cohort_month, cohort_year, cohort_quarter

ORDER BY cohort_year DESC, cohort_quarter DESC, cohort_month DESC

LIMIT 24;  -- Last 24 months

-- ============================================================================
-- Cohort Performance by Grade
-- ============================================================================

SELECT 
    cohort_year,
    cohort_quarter,
    loan_grade,
    
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amount), 2) AS total_volume,
    
    SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    ROUND(AVG(total_interest_received), 2) AS avg_interest_received,
    ROUND(AVG(months_since_issue), 1) AS avg_maturity_months

FROM monthly_cohorts

GROUP BY cohort_year, cohort_quarter, loan_grade

ORDER BY cohort_year DESC, cohort_quarter DESC, default_rate_pct DESC;

-- ============================================================================
-- Cohort Performance by Customer Segment
-- ============================================================================

SELECT 
    cohort_year,
    customer_segment,
    
    COUNT(*) AS total_loans,
    ROUND(SUM(loan_amount), 2) AS total_volume,
    
    SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    
    ROUND(AVG(total_payment), 2) AS avg_total_payment,
    ROUND(SUM(total_interest_received), 2) AS total_interest_income

FROM monthly_cohorts

GROUP BY cohort_year, customer_segment

ORDER BY cohort_year DESC, default_rate_pct DESC;

-- ============================================================================
-- Cumulative Default Curve
-- ============================================================================
-- Shows how defaults accumulate over loan lifetime

SELECT 
    months_since_issue,
    COUNT(*) AS loans_at_month,
    SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) AS cumulative_defaults,
    ROUND(100.0 * SUM(CASE WHEN is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS cumulative_default_rate_pct

FROM monthly_cohorts

WHERE cohort_year = 2017  -- Example: 2017 vintage

GROUP BY months_since_issue

ORDER BY months_since_issue;
