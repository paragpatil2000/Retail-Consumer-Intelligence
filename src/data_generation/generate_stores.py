import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

NUM_STORES = 50

states_cities = {
    "Maharashtra": ["Mumbai", "Pune", "Nashik", "Nagpur"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore"],
    "Delhi": ["New Delhi"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Telangana": ["Hyderabad"],
    "West Bengal": ["Kolkata"],
    "Rajasthan": ["Jaipur", "Jodhpur"],
    "Uttar Pradesh": ["Lucknow", "Noida"],
    "Madhya Pradesh": ["Indore", "Bhopal"]
}

regions = {
    "Maharashtra": "West",
    "Gujarat": "West",
    "Karnataka": "South",
    "Delhi": "North",
    "Tamil Nadu": "South",
    "Telangana": "South",
    "West Bengal": "East",
    "Rajasthan": "North",
    "Uttar Pradesh": "North",
    "Madhya Pradesh": "Central"
}

store_types = [
    "Hypermarket",
    "Supermarket",
    "Convenience Store",
    "Mini Mart",
    "Department Store"
]

stores = []

for store_id in range(1, NUM_STORES + 1):

    state = random.choice(list(states_cities.keys()))
    city = random.choice(states_cities[state])
    region = regions[state]

    store_type = random.choice(store_types)

    # Store size based on store type
    if store_type == "Hypermarket":
        area_sqft = random.randint(30000, 80000)
        daily_footfall = random.randint(800, 2500)
        total_employees = random.randint(50, 150)

    elif store_type == "Supermarket":
        area_sqft = random.randint(10000, 35000)
        daily_footfall = random.randint(400, 1500)
        total_employees = random.randint(20, 80)

    elif store_type == "Department Store":
        area_sqft = random.randint(15000, 50000)
        daily_footfall = random.randint(500, 1800)
        total_employees = random.randint(30, 100)

    elif store_type == "Mini Mart":
        area_sqft = random.randint(2000, 8000)
        daily_footfall = random.randint(100, 500)
        total_employees = random.randint(5, 20)

    else:
        area_sqft = random.randint(1000, 5000)
        daily_footfall = random.randint(80, 400)
        total_employees = random.randint(4, 15)

    store_name = f"{city} {store_type} {store_id}"

    pincode = str(random.randint(400000, 799999))

    opening_date = fake.date_between(
        start_date="-10y",
        end_date="-6m"
    )

    parking_available = random.choice([True, False])

    stores.append({
        "store_id": store_id,
        "store_name": store_name,
        "store_type": store_type,
        "city": city,
        "state": state,
        "region": region,
        "pincode": pincode,
        "area_sqft": area_sqft,
        "opening_date": opening_date,
        "daily_footfall": daily_footfall,
        "total_employees": total_employees,
        "parking_available": parking_available
    })
    
    stores_df = pd.DataFrame(stores)

import os
os.makedirs("data/raw", exist_ok=True)

output_path = "data/raw/stores.csv"

stores_df.to_csv(output_path, index=False)

print(f"Generated {len(stores_df):,} stores")
print(f"Saved to: {output_path}")
print("\nSample data:")
print(stores_df.head())

