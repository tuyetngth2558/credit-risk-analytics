-- ============================================================================
-- Default Analysis by Segment
-- ============================================================================
-- Purpose: Analyze default rates across different customer segments
-- Business Use: Identify high-risk segments for targeted interventions
-- ============================================================================

WITH segment_metrics AS (
    SELECT 
        c.customer_segment,
        c.risk_category,
        p.loan_grade,
        
        -- Volume metrics
        COUNT(DISTINCT f.loan_id) AS total_loans,
        COUNT(DISTINCT f.customer_id) AS total_customers,
        SUM(f.loan_amount) AS total_loan_volume,
        
        -- Default metrics
        SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS default_count,
        SUM(CASE WHEN f.is_default = TRUE THEN f.loan_amount ELSE 0 END) AS default_volume,
        
        -- Performance metrics
        AVG(f.interest_rate) AS avg_interest_rate,
        AVG(f.risk_score) AS avg_risk_score,
        AVG(c.fico_score) AS avg_fico_score,
        AVG(c.dti_ratio) AS avg_dti_ratio
        
    FROM fact_loans f
    INNER JOIN dim_customers c ON f.customer_id = c.customer_id
    INNER JOIN dim_products p ON f.product_id = p.product_id
    
    GROUP BY c.customer_segment, c.risk_category, p.loan_grade
)

SELECT 
    customer_segment,
    risk_category,
    loan_grade,
    
    -- Volume
    total_loans,
    total_customers,
    ROUND(total_loan_volume, 2) AS total_loan_volume,
    
    -- Default rates
    default_count,
    ROUND(100.0 * default_count / NULLIF(total_loans, 0), 2) AS default_rate_pct,
    ROUND(default_volume, 2) AS default_volume,
    ROUND(100.0 * default_volume / NULLIF(total_loan_volume, 0), 2) AS default_volume_pct,
    
    -- Average metrics
    ROUND(avg_interest_rate, 2) AS avg_interest_rate,
    ROUND(avg_risk_score, 2) AS avg_risk_score,
    ROUND(avg_fico_score, 0) AS avg_fico_score,
    ROUND(avg_dti_ratio, 2) AS avg_dti_ratio

FROM segment_metrics

ORDER BY default_rate_pct DESC, total_loan_volume DESC;

-- ============================================================================
-- Additional Analysis: Default Rate by FICO Category
-- ============================================================================

SELECT 
    c.fico_category,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate

FROM fact_loans f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY c.fico_category
ORDER BY default_rate_pct DESC;

-- ============================================================================
-- Additional Analysis: Default Rate by DTI Bucket
-- ============================================================================

SELECT 
    c.dti_bucket,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN f.is_default = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct,
    ROUND(AVG(c.credit_utilization), 2) AS avg_credit_utilization,
    ROUND(AVG(f.risk_score), 2) AS avg_risk_score

FROM fact_loans f
INNER JOIN dim_customers c ON f.customer_id = c.customer_id

GROUP BY c.dti_bucket
ORDER BY default_rate_pct DESC;
