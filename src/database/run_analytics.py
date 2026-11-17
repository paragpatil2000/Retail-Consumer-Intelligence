import sqlite3
import pandas as pd

DB_PATH = "data/retail_consumer.db"

conn = sqlite3.connect(DB_PATH)


# =========================================================
# 1. BUSINESS OVERVIEW
# =========================================================

query = """
SELECT
    COUNT(*) AS total_transactions,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS average_transaction_value
FROM transactions
WHERE return_flag = 0;
"""

result = pd.read_sql_query(query, conn)

print("\n========== BUSINESS OVERVIEW ==========\n")
print(result.to_string(index=False))


# =========================================================
# 2. TOP 10 PRODUCTS
# =========================================================

query = """
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
"""

result = pd.read_sql_query(query, conn)

print("\n========== TOP 10 PRODUCTS ==========\n")
print(result.to_string(index=False))


# =========================================================
# 3. CATEGORY PERFORMANCE
# =========================================================

query = """
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
"""

result = pd.read_sql_query(query, conn)

print("\n========== CATEGORY PERFORMANCE ==========\n")
print(result.to_string(index=False))


# =========================================================
# 4. MONTHLY SALES TREND
# =========================================================

query = """
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
"""

result = pd.read_sql_query(query, conn)

print("\n========== MONTHLY SALES TREND ==========\n")
print(result.to_string(index=False))


# =========================================================
# 5. STORE PERFORMANCE
# =========================================================

query = """
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
"""

result = pd.read_sql_query(query, conn)

print("\n========== STORE PERFORMANCE ==========\n")
print(result.to_string(index=False))


# =========================================================
# 6. SALES CHANNEL PERFORMANCE
# =========================================================

query = """
SELECT
    sales_channel,
    COUNT(transaction_id) AS transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM transactions
WHERE return_flag = 0
GROUP BY sales_channel
ORDER BY revenue DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n========== SALES CHANNEL PERFORMANCE ==========\n")
print(result.to_string(index=False))

# =========================================================
# 7. PROMOTION VS NON-PROMOTION PERFORMANCE
# =========================================================

query = """
SELECT
    CASE
        WHEN promotion_id IS NULL THEN 'No Promotion'
        ELSE 'Promotion'
    END AS promotion_status,
    COUNT(transaction_id) AS transactions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM transactions
WHERE return_flag = 0
GROUP BY promotion_status;
"""

result = pd.read_sql_query(query, conn)

print("\n========== PROMOTION VS NON-PROMOTION ==========\n")
print(result.to_string(index=False))


# =========================================================
# 8. PROMOTION PERFORMANCE BY CAMPAIGN TYPE
# =========================================================

query = """
SELECT
    p.campaign_type,
    COUNT(t.transaction_id) AS transactions,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS revenue,
    ROUND(AVG(t.discount_percent), 2) AS avg_discount
FROM transactions t
JOIN promotions p
    ON t.promotion_id = p.promotion_id
WHERE t.return_flag = 0
GROUP BY p.campaign_type
ORDER BY revenue DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n========== PROMOTION BY CAMPAIGN TYPE ==========\n")
print(result.to_string(index=False))


# =========================================================
# 9. PROMOTION PERFORMANCE BY CATEGORY
# =========================================================

query = """
SELECT
    pr.target_category AS category,
    COUNT(t.transaction_id) AS transactions,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS revenue,
    ROUND(AVG(t.discount_percent), 2) AS avg_discount
FROM transactions t
JOIN promotions pr
    ON t.promotion_id = pr.promotion_id
WHERE t.return_flag = 0
GROUP BY pr.target_category
ORDER BY revenue DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n========== PROMOTION BY CATEGORY ==========\n")
print(result.to_string(index=False))


# =========================================================
# 10. PROMOTION PERFORMANCE BY ADVERTISING CHANNEL
# =========================================================

query = """
SELECT
    p.advertising_channel,
    COUNT(t.transaction_id) AS transactions,
    SUM(t.quantity) AS units_sold,
    ROUND(SUM(t.total_amount), 2) AS revenue,
    ROUND(AVG(t.discount_percent), 2) AS avg_discount
FROM transactions t
JOIN promotions p
    ON t.promotion_id = p.promotion_id
WHERE t.return_flag = 0
GROUP BY p.advertising_channel
ORDER BY revenue DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n========== PROMOTION BY ADVERTISING CHANNEL ==========\n")
print(result.to_string(index=False))
# =========================================================
# CLOSE DATABASE
# =========================================================

conn.close()

print("\n========================================")
print("ALL ANALYTICS QUERIES EXECUTED!")
print("========================================")