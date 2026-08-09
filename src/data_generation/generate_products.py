import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

NUM_PRODUCTS = 500

categories = {
    "Beverages": {
        "sub_categories": ["Soft Drinks", "Juices", "Energy Drinks", "Tea", "Coffee"],
        "brands": ["Coca-Cola", "Pepsi", "Real", "Red Bull", "Tata Tea", "Nescafe"]
    },
    "Snacks": {
        "sub_categories": ["Chips", "Biscuits", "Namkeen", "Chocolates"],
        "brands": ["Lay's", "Parle", "Haldiram", "Cadbury", "Britannia"]
    },
    "Personal Care": {
        "sub_categories": ["Shampoo", "Soap", "Toothpaste", "Skin Care"],
        "brands": ["Dove", "Lux", "Himalaya", "Colgate", "Patanjali"]
    },
    "Home Care": {
        "sub_categories": ["Detergent", "Dishwash", "Floor Cleaner"],
        "brands": ["Surf Excel", "Ariel", "Vim", "Harpic"]
    },
    "Staples": {
        "sub_categories": ["Rice", "Wheat", "Dal", "Cooking Oil"],
        "brands": ["Fortune", "Aashirvaad", "Tata", "India Gate"]
    },
    "Dairy": {
        "sub_categories": ["Milk", "Curd", "Butter", "Cheese"],
        "brands": ["Amul", "Mother Dairy", "Milky Mist"]
    }
}

products = []

for product_id in range(1, NUM_PRODUCTS + 1):

    category = random.choice(list(categories.keys()))

    sub_category = random.choice(
        categories[category]["sub_categories"]
    )

    brand = random.choice(
        categories[category]["brands"]
    )

    # Generate realistic product name
    product_name = f"{brand} {sub_category} {random.randint(100, 999)}"

    # Category-based pack sizes
    if category in ["Beverages", "Dairy"]:
        package_size = random.choice([200, 250, 500, 750, 1000])
        unit = "ml"

    elif category in ["Snacks", "Staples"]:
        package_size = random.choice([100, 200, 500, 1000, 2000])
        unit = "g"

    else:
        package_size = random.choice([100, 200, 250, 500, 750, 1000])
        unit = "g"

    # Generate MRP
    mrp = round(random.uniform(20, 1500), 2)

    # Cost price is lower than MRP
    cost_price = round(
        mrp * random.uniform(0.55, 0.75),
        2
    )

    # Selling price slightly below MRP
    selling_price = round(
        mrp * random.uniform(0.85, 1.00),
        2
    )

    # GST based on product category
    if category in ["Staples", "Dairy"]:
        gst_percent = random.choice([0, 5])
    elif category in ["Personal Care", "Home Care"]:
        gst_percent = random.choice([12, 18])
    else:
        gst_percent = random.choice([5, 12, 18])

    # Shelf life
    if category == "Dairy":
        shelf_life_days = random.randint(5, 30)
    elif category == "Beverages":
        shelf_life_days = random.randint(90, 365)
    else:
        shelf_life_days = random.randint(90, 730)

    products.append({
        "product_id": product_id,
        "product_name": product_name,
        "brand": brand,
        "category": category,
        "sub_category": sub_category,
        "package_size": package_size,
        "unit": unit,
        "mrp": mrp,
        "cost_price": cost_price,
        "selling_price": selling_price,
        "gst_percent": gst_percent,
        "shelf_life_days": shelf_life_days
    })
    
    # Convert list to DataFrame
products_df = pd.DataFrame(products)

# Create output directory
import os

os.makedirs("data/raw", exist_ok=True)

# Save product data
output_path = "data/raw/products.csv"

products_df.to_csv(output_path, index=False)

print(f"Generated {len(products_df):,} products")
print(f"Saved to: {output_path}")
print("\nSample data:")
print(products_df.head())
