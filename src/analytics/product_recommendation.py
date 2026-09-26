import pandas as pd

RULES_PATH = "data/processed/association_rules.csv"
PRODUCT_PATH = "data/raw/products.csv"

OUTPUT_PATH = "data/processed/product_recommendations.csv"


# =========================================================
# 1. LOAD DATA
# =========================================================

print("Loading association rules...")

rules = pd.read_csv(RULES_PATH)
products = pd.read_csv(PRODUCT_PATH)

print(f"Association rules: {len(rules):,}")
print(f"Products: {len(products):,}")


# =========================================================
# 2. STANDARDIZE PRODUCT IDs
# =========================================================

# Convert IDs to string in both datasets
# This prevents merge datatype mismatch.

products["product_id"] = (
    products["product_id"]
    .astype(str)
    .str.strip()
)

rules["antecedents"] = (
    rules["antecedents"]
    .astype(str)
    .str.strip()
)

rules["consequents"] = (
    rules["consequents"]
    .astype(str)
    .str.strip()
)


# =========================================================
# 3. PRODUCT LOOKUP
# =========================================================

product_lookup = (
    products[
        [
            "product_id",
            "product_name",
            "brand",
            "category",
            "sub_category"
        ]
    ]
    .drop_duplicates("product_id")
)


# =========================================================
# 4. CREATE RECOMMENDATIONS
# =========================================================

recommendations = []

for _, row in rules.iterrows():

    antecedents = str(row["antecedents"]).split(",")
    consequents = str(row["consequents"]).split(",")

    for product_id in antecedents:

        product_id = product_id.strip()

        for recommended_id in consequents:

            recommended_id = recommended_id.strip()

            recommendations.append(
                {
                    "product_id": product_id,
                    "recommended_product_id": recommended_id,
                    "support": row["support"],
                    "confidence": row["confidence"],
                    "lift": row["lift"]
                }
            )


recommendations_df = pd.DataFrame(
    recommendations
)


# =========================================================
# 5. STANDARDIZE RECOMMENDATION IDs
# =========================================================

recommendations_df["product_id"] = (
    recommendations_df["product_id"]
    .astype(str)
    .str.strip()
)

recommendations_df["recommended_product_id"] = (
    recommendations_df["recommended_product_id"]
    .astype(str)
    .str.strip()
)


# =========================================================
# 6. MAP SOURCE PRODUCT DETAILS
# =========================================================

recommendations_df = recommendations_df.merge(
    product_lookup,
    on="product_id",
    how="left"
)

recommendations_df = recommendations_df.rename(
    columns={
        "brand": "product_brand",
        "category": "product_category",
        "sub_category": "product_sub_category"
    }
)


# =========================================================
# 7. MAP RECOMMENDED PRODUCT DETAILS
# =========================================================

recommended_lookup = product_lookup.rename(
    columns={
        "product_id": "recommended_product_id",
        "product_name": "recommended_product_name",
        "brand": "recommended_brand",
        "category": "recommended_category",
        "sub_category": "recommended_sub_category"
    }
)


recommendations_df = recommendations_df.merge(
    recommended_lookup,
    on="recommended_product_id",
    how="left"
)


# =========================================================
# 8. SORT
# =========================================================

recommendations_df = recommendations_df.sort_values(
    ["product_id", "lift", "confidence"],
    ascending=[True, False, False]
)


# =========================================================
# 9. REMOVE DUPLICATES
# =========================================================

recommendations_df = recommendations_df.drop_duplicates(
    subset=[
        "product_id",
        "recommended_product_id"
    ]
)


# =========================================================
# 10. SAVE
# =========================================================

recommendations_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# =========================================================
# 11. DISPLAY RESULTS
# =========================================================

print("\n========== TOP PRODUCT RECOMMENDATIONS ==========\n")

display_columns = [
    "product_id",
    "product_name",
    "recommended_product_id",
    "recommended_product_name",
    "recommended_brand",
    "recommended_category",
    "confidence",
    "lift"
]

print(
    recommendations_df[
        display_columns
    ]
    .head(20)
    .to_string(index=False)
)


# =========================================================
# 12. FINAL SUMMARY
# =========================================================

print("\n========================================")
print("PRODUCT RECOMMENDATION ENGINE COMPLETED!")
print("========================================")

print(
    f"\nTotal recommendations: "
    f"{len(recommendations_df):,}"
)

print(
    f"Products with recommendations: "
    f"{recommendations_df['product_id'].nunique():,}"
)

print("\nResults saved:")
print(OUTPUT_PATH)