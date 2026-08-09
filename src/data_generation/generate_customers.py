import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta


fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)

NUM_CUSTOMERS = 100_000

genders = ["Male", "Female", "Other"]

marital_statuses = ["Single", "Married", "Divorced", "Widowed"]

education_levels = [
    "High School",
    "Graduate",
    "Post Graduate",
    "Professional"
]

occupations = [
    "Student",
    "IT Professional",
    "Business Owner",
    "Government Employee",
    "Private Employee",
    "Teacher",
    "Healthcare Professional",
    "Homemaker",
    "Retired"
]

cities_by_state = {
    "Maharashtra": ["Mumbai", "Pune", "Nashik", "Nagpur", "Aurangabad"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore"],
    "Delhi": ["New Delhi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Telangana": ["Hyderabad"],
    "West Bengal": ["Kolkata"],
    "Rajasthan": ["Jaipur", "Jodhpur"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
    "Madhya Pradesh": ["Indore", "Bhopal"]
}

states = list(cities_by_state.keys())

regions = {
    "Maharashtra": "West",
    "Gujarat": "West",
    "Karnataka": "South",
    "Tamil Nadu": "South",
    "Telangana": "South",
    "Delhi": "North",
    "Rajasthan": "North",
    "Uttar Pradesh": "North",
    "Madhya Pradesh": "Central",
    "West Bengal": "East"
}

membership_types = ["Basic", "Silver", "Gold", "Platinum"]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking",
    "Wallet"
]

channels = [
    "Store",
    "Website",
    "Mobile App"
]

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    age = random.randint(18, 70)

    gender = random.choices(
        genders,
        weights=[48, 50, 2],
        k=1
    )[0]

    marital_status = random.choices(
        marital_statuses,
        weights=[35, 55, 7, 3],
        k=1
    )[0]

    education = random.choices(
        education_levels,
        weights=[15, 45, 25, 15],
        k=1
    )[0]

    occupation = random.choice(occupations)

    # Income based on occupation
    if occupation == "Student":
        annual_income = random.randint(100_000, 400_000)
    elif occupation == "Homemaker":
        annual_income = random.randint(150_000, 600_000)
    elif occupation == "Retired":
        annual_income = random.randint(300_000, 900_000)
    elif occupation == "IT Professional":
        annual_income = random.randint(500_000, 2_500_000)
    elif occupation == "Business Owner":
        annual_income = random.randint(400_000, 3_000_000)
    elif occupation == "Healthcare Professional":
        annual_income = random.randint(600_000, 2_500_000)
    else:
        annual_income = random.randint(300_000, 1_500_000)

    state = random.choice(states)
    city = random.choice(cities_by_state[state])
    region = regions[state]

    family_size = random.randint(1, 6)

    if age < 25:
        children = 0
    elif age < 35:
        children = random.choices([0, 1, 2], weights=[50, 35, 15])[0]
    else:
        children = random.choices([0, 1, 2, 3], weights=[10, 30, 45, 15])[0]

    membership_type = random.choices(
        membership_types,
        weights=[50, 30, 15, 5],
        k=1
    )[0]

    preferred_payment = random.choice(payment_methods)

    if age < 30:
        preferred_channel = random.choices(
            channels,
            weights=[25, 30, 45],
            k=1
        )[0]
    else:
        preferred_channel = random.choices(
            channels,
            weights=[55, 25, 20],
            k=1
        )[0]

    join_date = fake.date_between(
        start_date="-5y",
        end_date="today"
    )

    customers.append({
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": age,
        "gender": gender,
        "marital_status": marital_status,
        "education": education,
        "occupation": occupation,
        "annual_income": annual_income,
        "family_size": family_size,
        "children": children,
        "city": city,
        "state": state,
        "region": region,
        "membership_type": membership_type,
        "join_date": join_date,
        "preferred_payment": preferred_payment,
        "preferred_channel": preferred_channel
    })
    
    # Convert list to DataFrame
customers_df = pd.DataFrame(customers)

# Create output directory
import os

os.makedirs("data/raw", exist_ok=True)

# Save customer data
output_path = "data/raw/customers.csv"

customers_df.to_csv(output_path, index=False)

print(f"Generated {len(customers_df):,} customers")
print(f"Saved to: {output_path}")
print("\nSample data:")
print(customers_df.head())