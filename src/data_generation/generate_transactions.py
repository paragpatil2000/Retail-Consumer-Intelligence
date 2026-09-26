import os
import random
from datetime import datetime

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# 1. SETTINGS
# ---------------------------------------------------------

random.seed(42)
np.random.seed(42)

NUM_TRANSACTIONS = 1_000_000
BATCH_SIZE = 100_000

START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2026-07-31")

OUTPUT_PATH = "data/raw/transactions.csv"


# ---------------------------------------------------------
# 2. LOAD DIMENSION DATA
# ---------------------------------------------------------

customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
stores = pd.read_csv("data/raw/stores.csv")
promotions = pd.read_csv("data/raw/promotions.csv")


# ---------------------------------------------------------
# 3. ID ARRAYS
# ---------------------------------------------------------

customer_ids = customers["customer_id"].values
product_ids = products["product_id"].values
store_ids = stores["store_id"].values
promotion_ids = promotions["promotion_id"].values


# ---------------------------------------------------------
# 4. PAYMENT & SALES CHANNELS
# ---------------------------------------------------------

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking",
    "Wallet"
]

sales_channels = [
    "Store",
    "Website",
    "Mobile App"
]


# ---------------------------------------------------------
# 5. PRODUCT LOOKUP
# ---------------------------------------------------------

product_lookup = (
    products
    .set_index("product_id")
    [["mrp", "selling_price", "category"]]
    .to_dict("index")
)


# ---------------------------------------------------------
# 6. PROMOTION LOOKUP
# ---------------------------------------------------------

promotion_lookup = (
    promotions
    .set_index("promotion_id")
    [["discount_percent"]]
    .to_dict("index")
)


# ---------------------------------------------------------
# 7. PREPARE OUTPUT FILE
# ---------------------------------------------------------

os.makedirs("data/raw", exist_ok=True)

# Delete old transactions file if it exists
if os.path.exists(OUTPUT_PATH):
    os.remove(OUTPUT_PATH)


# ---------------------------------------------------------
# 8. GENERATE TRANSACTIONS IN BATCHES
# ---------------------------------------------------------

for batch_start in range(
    0,
    NUM_TRANSACTIONS,
    BATCH_SIZE
):

    batch_end = min(
        batch_start + BATCH_SIZE,
        NUM_TRANSACTIONS
    )

    batch = []

    for transaction_id in range(
        batch_start + 1,
        batch_end + 1
    ):

        # ---------------------------------------------
        # Select customer, product and store
        # ---------------------------------------------

        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)
        store_id = random.choice(store_ids)

        # ---------------------------------------------
        # Product information
        # ---------------------------------------------

        product = product_lookup[product_id]

        mrp = float(product["mrp"])

        # ---------------------------------------------
        # Promotion
        # ---------------------------------------------

        if random.random() < 0.25:

            promotion_id = random.choice(
                promotion_ids
            )

            discount_percent = float(
                promotion_lookup[promotion_id][
                    "discount_percent"
                ]
            )

        else:

            promotion_id = None
            discount_percent = 0.0

        # ---------------------------------------------
        # Selling price after discount
        # ---------------------------------------------

        selling_price = round(
            mrp * (1 - discount_percent / 100),
            2
        )

        # ---------------------------------------------
        # Quantity
        # ---------------------------------------------

        quantity = random.choices(
            [1, 2, 3, 4, 5, 6],
            weights=[40, 25, 15, 10, 6, 4],
            k=1
        )[0]

        # ---------------------------------------------
        # Total amount
        # ---------------------------------------------

        total_amount = round(
            quantity * selling_price,
            2
        )

        # ---------------------------------------------
        # Transaction date
        # ---------------------------------------------

        random_days = random.randint(
            0,
            (END_DATE - START_DATE).days
        )

        transaction_date = (
            START_DATE
            + pd.Timedelta(days=random_days)
        )

        # ---------------------------------------------
        # Transaction time
        # ---------------------------------------------

        transaction_time = datetime(
            2024,
            1,
            1,
            random.randint(8, 21),
            random.randint(0, 59)
        ).time()

        # ---------------------------------------------
        # Payment method
        # ---------------------------------------------

        payment_method = random.choice(
            payment_methods
        )

        # ---------------------------------------------
        # Sales channel
        # ---------------------------------------------

        sales_channel = random.choice(
            sales_channels
        )

        # ---------------------------------------------
        # Coupon
        # ---------------------------------------------

        coupon_used = (
            promotion_id is not None
            and random.random() < 0.60
        )

        # ---------------------------------------------
        # Return
        # ---------------------------------------------

        return_flag = random.random() < 0.03

        # ---------------------------------------------
        # Add transaction
        # ---------------------------------------------

        batch.append({
            "transaction_id": transaction_id,
            "transaction_date": transaction_date.date(),
            "transaction_time": transaction_time,
            "customer_id": customer_id,
            "product_id": product_id,
            "store_id": store_id,
            "promotion_id": promotion_id,
            "quantity": quantity,
            "mrp": mrp,
            "selling_price": selling_price,
            "discount_percent": discount_percent,
            "total_amount": total_amount,
            "payment_method": payment_method,
            "sales_channel": sales_channel,
            "coupon_used": coupon_used,
            "return_flag": return_flag
        })

    # -----------------------------------------------------
    # Convert only current batch to DataFrame
    # -----------------------------------------------------

    batch_df = pd.DataFrame(batch)

    # -----------------------------------------------------
    # Save current batch to CSV
    # -----------------------------------------------------

    batch_df.to_csv(
        OUTPUT_PATH,
        mode="a",
        header=(batch_start == 0),
        index=False
    )

    # -----------------------------------------------------
    # Progress
    # -----------------------------------------------------

    print(
        f"Generated {batch_end:,} / "
        f"{NUM_TRANSACTIONS:,} transactions"
    )

    # Free memory
    del batch
    del batch_df


# ---------------------------------------------------------
# 9. COMPLETION MESSAGE
# ---------------------------------------------------------

print()
print("Transaction generation completed successfully!")
print(f"Total transactions: {NUM_TRANSACTIONS:,}")
print(f"Saved to: {OUTPUT_PATH}")