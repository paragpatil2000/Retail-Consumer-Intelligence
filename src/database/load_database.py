import os
import sqlite3
import pandas as pd


# =========================================================
# 1. PATHS
# =========================================================

DB_PATH = "data/retail_consumer.db"
SCHEMA_PATH = "sql/database_schema.sql"
DATA_PATH = "data/raw"


# =========================================================
# 2. CREATE DATA FOLDER
# =========================================================

os.makedirs("data", exist_ok=True)


# =========================================================
# 3. DELETE OLD DATABASE
# =========================================================

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Old database removed.")


# =========================================================
# 4. CONNECT TO SQLITE
# =========================================================

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


# =========================================================
# 5. EXECUTE SQL SCHEMA
# =========================================================

print("\nCreating database schema...")

with open(
    SCHEMA_PATH,
    "r",
    encoding="utf-8"
) as file:

    schema = file.read()

cursor.executescript(schema)

print("Database schema created successfully.")


# =========================================================
# 6. CSV FILES
# =========================================================

files = {
    "customers": "customers.csv",
    "products": "products.csv",
    "stores": "stores.csv",
    "promotions": "promotions.csv",
    "calendar": "calendar.csv",
    "transactions": "transactions.csv"
}


# =========================================================
# 7. LOAD DATA
# =========================================================

print("\nLoading CSV data...\n")


for table_name, file_name in files.items():

    file_path = os.path.join(
        DATA_PATH,
        file_name
    )

    print(f"Loading {table_name}...")

    df = pd.read_csv(file_path)

    # Convert NaN to None for SQLite
    df = df.where(
        pd.notnull(df),
        None
    )

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False,
        chunksize=10_000
    )

    print(
        f"✓ {table_name}: "
        f"{len(df):,} rows loaded"
    )


# =========================================================
# 8. COMMIT
# =========================================================

conn.commit()


# =========================================================
# 9. VERIFY TABLES
# =========================================================

print("\nChecking tables...\n")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""")

tables = cursor.fetchall()

for table in tables:
    print("✓", table[0])


# =========================================================
# 10. ROW COUNT VALIDATION
# =========================================================

print("\nRow count validation:\n")


for table_name in files.keys():

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table_name}: {count:,}"
    )


# =========================================================
# 11. FOREIGN KEY VALIDATION
# =========================================================

print("\nChecking foreign keys...")

cursor.execute("""
    PRAGMA foreign_key_check;
""")

fk_errors = cursor.fetchall()


if len(fk_errors) == 0:

    print("✓ Foreign key validation passed.")

else:

    print("✗ Foreign key errors found:")
    print(fk_errors)


# =========================================================
# 12. CLOSE DATABASE
# =========================================================

conn.close()


# =========================================================
# 13. FINAL MESSAGE
# =========================================================

print("\n========================================")
print("DATABASE CREATED SUCCESSFULLY!")
print("========================================")

print(f"Database: {DB_PATH}")