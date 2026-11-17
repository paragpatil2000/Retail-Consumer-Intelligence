-- =========================================================
-- RETAIL CONSUMER INTELLIGENCE
-- SQL ANALYTICS QUERIES
-- =========================================================


-- =========================================================
-- 1. TOTAL SALES & TRANSACTIONS
-- =========================================================

SELECT
    COUNT(*) AS total_transactions,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS average_transaction_value
FROM transactions
WHERE return_flag = 0;


-- =========================================================
-- 2. MONTHLY SALES TREND
-- =========================================================

SELECT
    c.year,
    c.month,
    c.month_name,
    ROUND(SUM(t.total_amount), 2) AS revenue,
    SUM(t.quantity) AS units_sold,
    COUNT(t.transaction_id) AS transactions
FROM transactions t
JOIN calendar c
    ON t.transaction_date = c.date
WHERE t.return_flag = 0
GROUP BY
    c.year,
    c.month,
    c.month_name
ORDER BY
    c.year,
    c.month;


-- =========================================================
-- 3. TOP 10 PRODUCTS BY REVENUE
-- =========================================================

SELECT
    p.product_id,
    p.product_name,
    p.brand,
    p.category,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS revenue
FROM transactions t
JOIN products p
    ON t.product_id = p.product_id
WHERE t.return_flag = 0
GROUP BY
    p.product_id,
    p.product_name,
    p.brand,
    p.category
ORDER BY revenue DESC
LIMIT 10;


-- =========================================================
-- 4. CATEGORY PERFORMANCE
-- =========================================================

SELECT
    p.category,
    COUNT(t.transaction_id) AS transactions,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_transaction_value
FROM transactions t
JOIN products p
    ON t.product_id = p.product_id
WHERE t.return_flag = 0
GROUP BY p.category
ORDER BY revenue DESC;


-- =========================================================
-- 5. STORE PERFORMANCE
-- =========================================================

SELECT
    s.store_id,
    s.store_name,
    s.city,
    s.state,
    s.region,
    COUNT(t.transaction_id) AS transactions,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS revenue
FROM transactions t
JOIN stores s
    ON t.store_id = s.store_id
WHERE t.return_flag = 0
GROUP BY
    s.store_id,
    s.store_name,
    s.city,
    s.state,
    s.region
ORDER BY revenue DESC;
