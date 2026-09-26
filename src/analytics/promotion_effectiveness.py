import sqlite3
import pandas as pd

DB_PATH = "data/retail_consumer.db"

OUTPUT_PATH = (
    "data/processed/promotion_effectiveness.csv"
)


# =========================================================
# 1. CONNECT DATABASE
# =========================================================

print("Connecting to database...")

conn = sqlite3.connect(DB_PATH)


# =========================================================
# 2. PROMOTION vs NON-PROMOTION
# =========================================================

print("\nAnalyzing promotion performance...")

query_promotion = """

SELECT
    CASE
        WHEN t.promotion_id IS NULL
        THEN 'No Promotion'
        ELSE 'Promotion'
    END AS promotion_status,

    COUNT(DISTINCT t.transaction_id)
        AS transactions,

    SUM(t.quantity)
        AS units_sold,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.total_amount
            ELSE 0
        END
    ) AS revenue,

    AVG(t.discount_percent)
        AS avg_discount

FROM transactions t

GROUP BY promotion_status

ORDER BY revenue DESC;

"""

promotion_summary = pd.read_sql_query(
    query_promotion,
    conn
)


# =========================================================
# 3. CAMPAIGN TYPE PERFORMANCE
# =========================================================

print("\nAnalyzing campaign types...")

query_campaign = """

SELECT

    p.campaign_type,

    COUNT(DISTINCT t.transaction_id)
        AS transactions,

    SUM(t.quantity)
        AS units_sold,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.total_amount
            ELSE 0
        END
    ) AS revenue,

    AVG(t.discount_percent)
        AS avg_discount

FROM transactions t

INNER JOIN promotions p
    ON t.promotion_id = p.promotion_id

GROUP BY p.campaign_type

ORDER BY revenue DESC;

"""

campaign_performance = pd.read_sql_query(
    query_campaign,
    conn
)


# =========================================================
# 4. CATEGORY PERFORMANCE
# =========================================================

print("\nAnalyzing category performance...")

query_category = """

SELECT

    p.category,

    COUNT(DISTINCT t.transaction_id)
        AS transactions,

    SUM(t.quantity)
        AS units_sold,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.total_amount
            ELSE 0
        END
    ) AS revenue,

    AVG(t.discount_percent)
        AS avg_discount

FROM transactions t

INNER JOIN promotions pr
    ON t.promotion_id = pr.promotion_id

INNER JOIN products p
    ON t.product_id = p.product_id

GROUP BY p.category

ORDER BY revenue DESC;

"""

category_performance = pd.read_sql_query(
    query_category,
    conn
)


# =========================================================
# 5. ADVERTISING CHANNEL PERFORMANCE
# =========================================================

print("\nAnalyzing advertising channels...")

query_channel = """

SELECT

    pr.advertising_channel,

    COUNT(DISTINCT t.transaction_id)
        AS transactions,

    SUM(t.quantity)
        AS units_sold,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.total_amount
            ELSE 0
        END
    ) AS revenue,

    AVG(t.discount_percent)
        AS avg_discount

FROM transactions t

INNER JOIN promotions pr
    ON t.promotion_id = pr.promotion_id

GROUP BY pr.advertising_channel

ORDER BY revenue DESC;

"""

channel_performance = pd.read_sql_query(
    query_channel,
    conn
)


# =========================================================
# 6. PROMOTION PERFORMANCE BY BRAND
# =========================================================

print("\nAnalyzing brand performance...")

query_brand = """

SELECT

    p.brand,

    COUNT(DISTINCT t.transaction_id)
        AS transactions,

    SUM(t.quantity)
        AS units_sold,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.total_amount
            ELSE 0
        END
    ) AS revenue,

    AVG(t.discount_percent)
        AS avg_discount

FROM transactions t

INNER JOIN promotions pr
    ON t.promotion_id = pr.promotion_id

INNER JOIN products p
    ON t.product_id = p.product_id

GROUP BY p.brand

ORDER BY revenue DESC;

"""

brand_performance = pd.read_sql_query(
    query_brand,
    conn
)


# =========================================================
# 7. CLOSE DATABASE
# =========================================================

conn.close()


# =========================================================
# 8. DISPLAY RESULTS
# =========================================================

print("\n========================================")
print("PROMOTION vs NON-PROMOTION")
print("========================================")

print(
    promotion_summary.to_string(
        index=False
    )
)


print("\n========================================")
print("CAMPAIGN TYPE PERFORMANCE")
print("========================================")

print(
    campaign_performance.to_string(
        index=False
    )
)


print("\n========================================")
print("CATEGORY PERFORMANCE")
print("========================================")

print(
    category_performance.to_string(
        index=False
    )
)


print("\n========================================")
print("ADVERTISING CHANNEL PERFORMANCE")
print("========================================")

print(
    channel_performance.to_string(
        index=False
    )
)


print("\n========================================")
print("TOP BRANDS UNDER PROMOTIONS")
print("========================================")

print(
    brand_performance.head(15).to_string(
        index=False
    )
)


# =========================================================
# 9. SAVE MAIN OUTPUT
# =========================================================

promotion_summary.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n========================================")
print("PROMOTION EFFECTIVENESS COMPLETED!")
print("========================================")

print(
    f"\nOutput saved to: {OUTPUT_PATH}"
)