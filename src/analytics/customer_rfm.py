import sqlite3
import pandas as pd

DB_PATH = "data/retail_consumer.db"

conn = sqlite3.connect(DB_PATH)

# =========================================================
# 1. CUSTOMER RFM DATA
# =========================================================

query = """
SELECT
    t.customer_id,
    MAX(t.transaction_date) AS last_purchase_date,
    COUNT(t.transaction_id) AS frequency,
    SUM(t.total_amount) AS monetary
FROM transactions t
WHERE t.return_flag = 0
GROUP BY t.customer_id;
"""

df = pd.read_sql_query(query, conn)

reference_date = pd.to_datetime(
    df["last_purchase_date"]
).max()

df["last_purchase_date"] = pd.to_datetime(
    df["last_purchase_date"]
)

df["recency"] = (
    reference_date - df["last_purchase_date"]
).dt.days

rfm = df[
    [
        "customer_id",
        "recency",
        "frequency",
        "monetary"
    ]
].copy()


# =========================================================
# 2. RFM SCORES
# =========================================================

rfm["R_score"] = pd.qcut(
    rfm["recency"],
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)


rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)


# =========================================================
# 3. CUSTOMER SEGMENTATION
# =========================================================

def assign_segment(row):

    r = row["R_score"]
    f = row["F_score"]
    m = row["M_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4 and m >= 3:
        return "Loyal Customers"

    elif r >= 4 and f >= 2 and m >= 2:
        return "Potential Loyalists"

    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2 and m <= 2:
        return "Lost Customers"

    else:
        return "Needs Attention"


rfm["segment"] = rfm.apply(
    assign_segment,
    axis=1
)


# =========================================================
# 4. CUSTOMER SEGMENT SUMMARY
# =========================================================

segment_summary = (
    rfm.groupby("segment")
    .agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean")
    )
    .reset_index()
)

segment_summary["avg_recency"] = (
    segment_summary["avg_recency"].round(2)
)

segment_summary["avg_frequency"] = (
    segment_summary["avg_frequency"].round(2)
)

segment_summary["avg_monetary"] = (
    segment_summary["avg_monetary"].round(2)
)


# =========================================================
# 5. DISPLAY RESULTS
# =========================================================

print("\n========== CUSTOMER SEGMENTS ==========\n")

print(
    rfm[
        [
            "customer_id",
            "recency",
            "frequency",
            "monetary",
            "RFM_score",
            "segment"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


print("\n========== SEGMENT SUMMARY ==========\n")

print(
    segment_summary
    .sort_values(
        "customers",
        ascending=False
    )
    .to_string(index=False)
)


# =========================================================
# 6. SAVE OUTPUT
# =========================================================

output_path = "data/processed/customer_rfm_segments.csv"

rfm.to_csv(
    output_path,
    index=False
)

print("\nRFM output saved to:")
print(output_path)


conn.close()

print("\n========================================")
print("CUSTOMER SEGMENTATION COMPLETED!")
print("========================================")