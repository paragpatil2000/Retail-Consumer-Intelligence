import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import timedelta

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

NUM_PROMOTIONS = 100

campaign_types = [
    "Discount",
    "Buy One Get One",
    "Coupon",
    "Bundle Offer",
    "Loyalty Offer",
    "Festival Offer"
]

festivals = [
    "Diwali",
    "Holi",
    "Eid",
    "Christmas",
    "Republic Day",
    "Independence Day",
    "New Year",
    "None"
]

advertising_channels = [
    "Social Media",
    "Email",
    "SMS",
    "TV",
    "In-Store",
    "Google Ads",
    "App Notification"
]

target_categories = [
    "Beverages",
    "Snacks",
    "Personal Care",
    "Home Care",
    "Staples",
    "Dairy"
]

promotions = []

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-12-31")

for promotion_id in range(1, NUM_PROMOTIONS + 1):

    campaign_type = random.choice(campaign_types)

    campaign_name = f"{campaign_type} Campaign {promotion_id}"

    promotion_start = fake.date_between(
        start_date=start_date.date(),
        end_date=end_date.date()
    )

    duration_days = random.randint(7, 45)

    promotion_end = promotion_start + timedelta(
        days=duration_days
    )

    discount_percent = random.choice(
        [5, 10, 15, 20, 25, 30, 40]
    )

    target_category = random.choice(target_categories)

    target_brand = None

    # Coupon campaigns get coupon codes
    if campaign_type in ["Coupon", "Festival Offer"]:
        coupon_code = f"SAVE{random.randint(1000, 9999)}"
    else:
        coupon_code = None

    festival = random.choice(festivals)

    promotion_budget = round(
        random.uniform(50_000, 2_000_000),
        2
    )

    advertising_channel = random.choice(
        advertising_channels
    )

    promotions.append({
        "promotion_id": promotion_id,
        "campaign_name": campaign_name,
        "campaign_type": campaign_type,
        "discount_percent": discount_percent,
        "start_date": promotion_start,
        "end_date": promotion_end,
        "target_category": target_category,
        "target_brand": target_brand,
        "coupon_code": coupon_code,
        "festival": festival,
        "promotion_budget": promotion_budget,
        "advertising_channel": advertising_channel
    })
    
    promotions_df = pd.DataFrame(promotions)

import os
os.makedirs("data/raw", exist_ok=True)

output_path = "data/raw/promotions.csv"

promotions_df.to_csv(
    output_path,
    index=False
)

print(f"Generated {len(promotions_df):,} promotions")
print(f"Saved to: {output_path}")

print("\nSample data:")
print(promotions_df.head())

