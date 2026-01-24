-- =====================================================
-- FRAUD DETECTION - SQL ANALYSIS QUERIES
-- Author: [Your Name]
-- Description: SQL queries for transaction analysis
-- =====================================================

-- =====================================================
-- 1. DATABASE SETUP
-- =====================================================

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    time_seconds INTEGER,
    v1 REAL, v2 REAL, v3 REAL, v4 REAL, v5 REAL,
    v6 REAL, v7 REAL, v8 REAL, v9 REAL, v10 REAL,
    v11 REAL, v12 REAL, v13 REAL, v14 REAL, v15 REAL,
    v16 REAL, v17 REAL, v18 REAL, v19 REAL, v20 REAL,
    v21 REAL, v22 REAL, v23 REAL, v24 REAL, v25 REAL,
    v26 REAL, v27 REAL, v28 REAL,
    amount REAL,
    is_fraud INTEGER,  -- 0 = Normal, 1 = Fraud
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX idx_fraud ON transactions(is_fraud);
CREATE INDEX idx_amount ON transactions(amount);
CREATE INDEX idx_time ON transactions(time_seconds);

-- =====================================================
-- 2. BASIC STATISTICS
-- =====================================================

-- Total transaction count
SELECT 
    COUNT(*) as total_transactions,
    COUNT(DISTINCT transaction_id) as unique_transactions
FROM transactions;

-- Fraud vs Normal distribution
SELECT 
    is_fraud,
    COUNT(*) as transaction_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as percentage
FROM transactions
GROUP BY is_fraud;

-- Amount statistics by fraud status
SELECT 
    is_fraud,
    COUNT(*) as count,
    ROUND(MIN(amount), 2) as min_amount,
    ROUND(AVG(amount), 2) as avg_amount,
    ROUND(MAX(amount), 2) as max_amount,
    ROUND(SUM(amount), 2) as total_amount
FROM transactions
GROUP BY is_fraud;

-- =====================================================
-- 3. TIME-BASED ANALYSIS
-- =====================================================

-- Transactions per hour
SELECT 
    (time_seconds / 3600) as hour,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(AVG(amount), 2) as avg_amount
FROM transactions
GROUP BY hour
ORDER BY hour;

-- Peak fraud hours
SELECT 
    (time_seconds / 3600) as hour,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_transactions,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_rate
FROM transactions
GROUP BY hour
HAVING fraud_transactions > 0
ORDER BY fraud_rate DESC
LIMIT 10;

-- =====================================================
-- 4. AMOUNT-BASED ANALYSIS
-- =====================================================

-- Amount distribution by ranges
SELECT 
    CASE 
        WHEN amount < 10 THEN '0-10'
        WHEN amount < 50 THEN '10-50'
        WHEN amount < 100 THEN '50-100'
        WHEN amount < 500 THEN '100-500'
        ELSE '500+'
    END as amount_range,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(AVG(amount), 2) as avg_amount
FROM transactions
GROUP BY amount_range
ORDER BY 
    CASE amount_range
        WHEN '0-10' THEN 1
        WHEN '10-50' THEN 2
        WHEN '50-100' THEN 3
        WHEN '100-500' THEN 4
        ELSE 5
    END;

-- High-value fraudulent transactions
SELECT 
    transaction_id,
    amount,
    time_seconds / 3600 as hour
FROM transactions
WHERE is_fraud = 1
ORDER BY amount DESC
LIMIT 20;

-- =====================================================
-- 5. PATTERN DETECTION QUERIES
-- =====================================================

-- Suspicious rapid transactions (same amount within 1 hour)
SELECT 
    t1.amount,
    COUNT(*) as occurrence_count,
    MIN(t1.time_seconds) as first_time,
    MAX(t1.time_seconds) as last_time
FROM transactions t1
JOIN transactions t2 
    ON t1.amount = t2.amount 
    AND ABS(t1.time_seconds - t2.time_seconds) <= 3600
    AND t1.transaction_id != t2.transaction_id
WHERE t1.is_fraud = 1
GROUP BY t1.amount
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;

-- Fraud concentration by amount percentile
WITH amount_percentiles AS (
    SELECT 
        transaction_id,
        amount,
        is_fraud,
        NTILE(10) OVER (ORDER BY amount) as percentile_group
    FROM transactions
)
SELECT 
    percentile_group,
    COUNT(*) as total_count,
    SUM(is_fraud) as fraud_count,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) as fraud_percentage,
    ROUND(MIN(amount), 2) as min_amount,
    ROUND(MAX(amount), 2) as max_amount
FROM amount_percentiles
GROUP BY percentile_group
ORDER BY percentile_group;

-- =====================================================
-- 6. ADVANCED ANALYTICS
-- =====================================================

-- Rolling fraud rate (per 1000 transactions)
WITH ordered_transactions AS (
    SELECT 
        transaction_id,
        is_fraud,
        ROW_NUMBER() OVER (ORDER BY time_seconds) as row_num
    FROM transactions
)
SELECT 
    CAST(row_num / 1000 AS INTEGER) as batch_number,
    COUNT(*) as transaction_count,
    SUM(is_fraud) as fraud_count,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) as fraud_rate
FROM ordered_transactions
GROUP BY CAST(row_num / 1000 AS INTEGER)
ORDER BY batch_number;

-- Cumulative fraud detection
SELECT 
    time_seconds / 3600 as hour,
    COUNT(*) as transactions_this_hour,
    SUM(COUNT(*)) OVER (ORDER BY time_seconds / 3600) as cumulative_transactions,
    SUM(is_fraud) as fraud_this_hour,
    SUM(SUM(is_fraud)) OVER (ORDER BY time_seconds / 3600) as cumulative_fraud
FROM transactions
GROUP BY hour
ORDER BY hour;

-- =====================================================
-- 7. DATA QUALITY CHECKS
-- =====================================================

-- Check for missing values
SELECT 
    'Amount' as field,
    COUNT(*) - COUNT(amount) as missing_count
FROM transactions
UNION ALL
SELECT 
    'Time' as field,
    COUNT(*) - COUNT(time_seconds) as missing_count
FROM transactions
UNION ALL
SELECT 
    'Fraud Flag' as field,
    COUNT(*) - COUNT(is_fraud) as missing_count
FROM transactions;

-- Duplicate transaction check
SELECT 
    time_seconds,
    amount,
    COUNT(*) as duplicate_count
FROM transactions
GROUP BY time_seconds, amount
HAVING COUNT(*) > 1;

-- =====================================================
-- 8. BUSINESS INSIGHTS
-- =====================================================

-- Total financial impact of fraud
SELECT 
    SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) as total_fraud_amount,
    SUM(CASE WHEN is_fraud = 0 THEN amount ELSE 0 END) as total_legitimate_amount,
    SUM(amount) as total_transaction_amount,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) * 100.0 / SUM(amount), 2) as fraud_amount_percentage
FROM transactions;

-- Average transaction value comparison
SELECT 
    'Fraudulent' as transaction_type,
    ROUND(AVG(amount), 2) as avg_amount,
    ROUND(STDDEV(amount), 2) as std_dev
FROM transactions
WHERE is_fraud = 1
UNION ALL
SELECT 
    'Legitimate' as transaction_type,
    ROUND(AVG(amount), 2) as avg_amount,
    ROUND(STDDEV(amount), 2) as std_dev
FROM transactions
WHERE is_fraud = 0;

-- =====================================================
-- 9. EXPORT QUERIES FOR VISUALIZATION
-- =====================================================

-- Export hourly fraud trends
CREATE VIEW hourly_fraud_trends AS
SELECT 
    (time_seconds / 3600) as hour,
    COUNT(*) as total_transactions,
    SUM(is_fraud) as fraud_transactions,
    ROUND(AVG(amount), 2) as avg_amount
FROM transactions
GROUP BY hour
ORDER BY hour;

-- Export amount distribution for visualization
CREATE VIEW amount_distribution AS
SELECT 
    is_fraud,
    amount,
    time_seconds
FROM transactions
ORDER BY RANDOM()
LIMIT 10000;  -- Sample for visualization