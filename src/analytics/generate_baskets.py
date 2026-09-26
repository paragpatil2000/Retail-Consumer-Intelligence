import pandas as pd
import numpy as np
import random

PRODUCT_PATH = "data/raw/products.csv"
CUSTOMER_PATH = "data/raw/customers.csv"
STORE_PATH = "data/raw/stores.csv"

OUTPUT_PATH = "data/processed/basket_transactions.csv"

NUM_BASKETS = 250_000

random.seed(42)
np.random.seed(42)


# =========================================================
# 1. LOAD MASTER DATA
# =========================================================

print("Loading master data...")

products = pd.read_csv(PRODUCT_PATH)
customers = pd.read_csv(CUSTOMER_PATH)
stores = pd.read_csv(STORE_PATH)

print(f"Products: {len(products):,}")
print(f"Customers: {len(customers):,}")
print(f"Stores: {len(stores):,}")


# =========================================================
# 2. PRODUCT POOLS BY CATEGORY
# =========================================================

category_products = {
    category: products[
        products["category"] == category
    ]["product_id"].tolist()
    for category in products["category"].unique()
}


# =========================================================
# 3. CREATE PRODUCT-LEVEL AFFINITY GROUPS
# =========================================================

# Pick popular products from each category.
# These products will repeatedly appear together.

def get_product(category, index=0):

    pool = category_products[category]

    return pool[index % len(pool)]


PRODUCT_BUNDLES = [

    # Beverages + Snacks
    [
        get_product("Beverages", 0),
        get_product("Snacks", 0),
    ],

    [
        get_product("Beverages", 1),
        get_product("Snacks", 1),
    ],

    [
        get_product("Beverages", 2),
        get_product("Snacks", 2),
    ],

    # Dairy + Beverages
    [
        get_product("Dairy", 0),
        get_product("Beverages", 3),
    ],

    [
        get_product("Dairy", 1),
        get_product("Beverages", 4),
    ],

    # Dairy + Staples
    [
        get_product("Dairy", 2),
        get_product("Staples", 0),
    ],

    [
        get_product("Dairy", 3),
        get_product("Staples", 1),
    ],

    # Staples + Home Care
    [
        get_product("Staples", 2),
        get_product("Home Care", 0),
    ],

    [
        get_product("Staples", 3),
        get_product("Home Care", 1),
    ],

    # Home Care + Personal Care
    [
        get_product("Home Care", 2),
        get_product("Personal Care", 0),
    ],

    [
        get_product("Personal Care", 1),
        get_product("Home Care", 3),
    ],
]


print(f"Product affinity bundles: {len(PRODUCT_BUNDLES)}")


# =========================================================
# 4. GENERATE BASKETS
# =========================================================

print("\nGenerating baskets...")

rows = []

all_product_ids = products["product_id"].tolist()
customer_ids = customers["customer_id"].tolist()
store_ids = stores["store_id"].tolist()

categories = list(category_products.keys())


for basket_id in range(1, NUM_BASKETS + 1):

    # -----------------------------------------------------
    # Basket size
    # -----------------------------------------------------

    basket_size = random.choices(
        [2, 3, 4, 5],
        weights=[20, 40, 30, 10]
    )[0]

    # -----------------------------------------------------
    # Customer / Store
    # -----------------------------------------------------

    customer_id = random.choice(customer_ids)
    store_id = random.choice(store_ids)

    # -----------------------------------------------------
    # Date
    # -----------------------------------------------------

    transaction_date = (
        pd.Timestamp("2024-01-01")
        + pd.Timedelta(
            days=random.randint(0, 940)
        )
    ).date()

    # -----------------------------------------------------
    # 60% baskets use predefined product affinity
    # -----------------------------------------------------

    if random.random() < 0.60:

        bundle = random.choice(PRODUCT_BUNDLES)

        selected_products = list(bundle)

        # Add remaining products
        while len(selected_products) < basket_size:

            product_id = random.choice(all_product_ids)

            if product_id not in selected_products:

                selected_products.append(product_id)

    else:

        # -------------------------------------------------
        # Random basket
        # -------------------------------------------------

        selected_products = random.sample(
            all_product_ids,
            basket_size
        )

    # -----------------------------------------------------
    # Create rows
    # -----------------------------------------------------

    for product_id in selected_products:

        quantity = random.choices(
            [1, 2, 3],
            weights=[70, 25, 5]
        )[0]

        rows.append(
            {
                "basket_id": basket_id,
                "transaction_date": transaction_date,
                "customer_id": customer_id,
                "store_id": store_id,
                "product_id": product_id,
                "quantity": quantity,
            }
        )

    # -----------------------------------------------------
    # Progress
    # -----------------------------------------------------

    if basket_id % 25_000 == 0:

        print(
            f"Generated {basket_id:,} / "
            f"{NUM_BASKETS:,} baskets"
        )


# =========================================================
# 5. CREATE DATAFRAME
# =========================================================

basket_df = pd.DataFrame(rows)


# =========================================================
# 6. VALIDATION
# =========================================================

print("\n========== VALIDATION ==========")

print(
    f"Total basket rows: "
    f"{len(basket_df):,}"
)

print(
    f"Unique baskets: "
    f"{basket_df['basket_id'].nunique():,}"
)

print(
    f"Unique products: "
    f"{basket_df['product_id'].nunique():,}"
)

basket_sizes = (
    basket_df
    .groupby("basket_id")["product_id"]
    .nunique()
)

print(
    f"Average products per basket: "
    f"{basket_sizes.mean():.2f}"
)

print(
    f"Minimum products per basket: "
    f"{basket_sizes.min()}"
)

print(
    f"Maximum products per basket: "
    f"{basket_sizes.max()}"
)


# =========================================================
# 7. SAVE
# =========================================================

basket_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nBasket data saved successfully!")

print(
    f"Output: {OUTPUT_PATH}"
)