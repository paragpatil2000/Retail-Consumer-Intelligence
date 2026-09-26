import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

INPUT_PATH = "data/processed/basket_transactions.csv"

print("Loading basket data...")

df = pd.read_csv(INPUT_PATH)

print(f"Basket rows: {len(df):,}")
print(f"Unique baskets: {df['basket_id'].nunique():,}")
print(f"Unique products: {df['product_id'].nunique():,}")


# =========================================================
# 1. CREATE PRODUCT LIST FOR EACH BASKET
# =========================================================

basket_data = (
    df.groupby("basket_id")["product_id"]
    .apply(lambda x: list(set(x)))
    .tolist()
)

print("\nCreating sparse basket matrix...")


# =========================================================
# 2. TRANSACTION ENCODING
# =========================================================

te = TransactionEncoder()

basket_array = te.fit(basket_data).transform(
    basket_data,
    sparse=True
)

basket_matrix = pd.DataFrame.sparse.from_spmatrix(
    basket_array,
    columns=te.columns_
)

basket_matrix.columns = basket_matrix.columns.astype(str)

print(f"Basket matrix shape: {basket_matrix.shape}")


# =========================================================
# 3. FP-GROWTH
# =========================================================

print("\nRunning FP-Growth...")

frequent_itemsets = fpgrowth(
    basket_matrix,
    min_support=0.0001,
    use_colnames=True
)

frequent_itemsets["item_count"] = (
    frequent_itemsets["itemsets"].apply(len)
)

frequent_itemsets = frequent_itemsets.sort_values(
    "support",
    ascending=False
)

print(
    f"Frequent itemsets found: "
    f"{len(frequent_itemsets):,}"
)


# =========================================================
# 4. ASSOCIATION RULES
# =========================================================

if len(frequent_itemsets) > 0:

    print("\nGenerating association rules...")

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=0.10
    )

    # Filter meaningful rules
    rules = rules[
        (rules["lift"] > 1.2)
        & (rules["confidence"] >= 0.10)
    ]

    # Sort by highest lift
    rules = rules.sort_values(
        "lift",
        ascending=False
    )

    # Convert product IDs to readable strings
    rules["antecedents"] = rules["antecedents"].apply(
        lambda x: ", ".join(map(str, x))
    )

    rules["consequents"] = rules["consequents"].apply(
        lambda x: ", ".join(map(str, x))
    )

    rules = rules[
        [
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift"
        ]
    ]

else:

    print("No frequent itemsets found.")

    rules = pd.DataFrame()


# =========================================================
# 5. SAVE RESULTS
# =========================================================

frequent_itemsets.to_csv(
    "data/processed/frequent_itemsets.csv",
    index=False
)

rules.to_csv(
    "data/processed/association_rules.csv",
    index=False
)


# =========================================================
# 6. DISPLAY RESULTS
# =========================================================

print("\n========== TOP FREQUENT ITEMSETS ==========\n")

print(
    frequent_itemsets.head(15).to_string(
        index=False
    )
)


print("\n========== TOP ASSOCIATION RULES ==========\n")

if len(rules) > 0:

    print(
        rules.head(20).to_string(
            index=False
        )
    )

else:

    print("No association rules generated.")


# =========================================================
# 7. FINAL SUMMARY
# =========================================================

print("\n========================================")
print("MARKET BASKET ANALYSIS COMPLETED!")
print("========================================")

print(
    f"\nFrequent itemsets: "
    f"{len(frequent_itemsets):,}"
)

print(
    f"Association rules: "
    f"{len(rules):,}"
)

print("\nResults saved:")

print("data/processed/frequent_itemsets.csv")
print("data/processed/association_rules.csv")