from pathlib import Path
import sqlite3
from fastapi import FastAPI
from pathlib import Path
import pandas as pd

app = FastAPI(
    title="Retail Consumer Intelligence API",
    description="Consumer, Sales, Promotion and Forecast Analytics API",
    version="1.0.0"
)

DB_PATH = Path("data/retail_consumer.db")


@app.get("/")
def root():
    return {
        "message": "Retail Consumer Intelligence API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/sales/summary")
def sales_summary():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        SUM(total_amount) AS total_sales,
        COUNT(DISTINCT transaction_id) AS total_transactions,
        SUM(quantity) AS total_units,
        AVG(total_amount) AS average_transaction_value
    FROM transactions
    WHERE return_flag = 0
    """

    result = conn.execute(query).fetchone()
    conn.close()

    return {
        "total_sales": round(result[0], 2),
        "total_transactions": result[1],
        "total_units": result[2],
        "average_transaction_value": round(result[3], 2)
    }
    
@app.get("/products/top")
def top_products(limit: int = 10):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        p.product_id,
        p.product_name,
        p.brand,
        p.category,
        SUM(t.quantity) AS units_sold,
        SUM(t.total_amount) AS total_sales
    FROM transactions t
    JOIN products p
        ON t.product_id = p.product_id
    WHERE t.return_flag = 0
    GROUP BY
        p.product_id,
        p.product_name,
        p.brand,
        p.category
    ORDER BY total_sales DESC
    LIMIT ?
    """

    rows = conn.execute(query, (limit,)).fetchall()
    conn.close()

    return {
        "top_products": [
            {
                "product_id": row[0],
                "product_name": row[1],
                "brand": row[2],
                "category": row[3],
                "units_sold": row[4],
                "total_sales": round(row[5], 2)
            }
            for row in rows
        ]
    }
@app.get("/customers/segments")
def customer_segments():

    file_path = Path("data/processed/customer_rfm_segments.csv")

    df = pd.read_csv(file_path)

    result = (
        df.groupby("segment")
        .size()
        .reset_index(name="customer_count")
        .sort_values("customer_count", ascending=False)
    )

    return {
        "customer_segments": result.to_dict(orient="records")
    }
@app.get("/promotions/effectiveness")
def promotion_effectiveness():

    file_path = Path("data/processed/promotion_effectiveness.csv")

    df = pd.read_csv(file_path)

    return {
        "promotion_effectiveness": df.to_dict(orient="records")
    }
@app.get("/forecast")
def sales_forecast(limit: int = 30):

    file_path = Path("data/processed/sales_forecast.csv")

    df = pd.read_csv(file_path)

    # Last forecast records
    df = df.tail(limit)

    return {
        "forecast": df.to_dict(orient="records")
    }
@app.get("/recommendations/{product_id}")
def product_recommendations(product_id: int):

    file_path = Path("data/processed/product_recommendations.csv")

    df = pd.read_csv(file_path)

    result = df[df["product_id"] == product_id]

    if result.empty:
        return {
            "product_id": product_id,
            "recommendations": []
        }

    return {
        "product_id": product_id,
        "recommendations": result.to_dict(orient="records")
    }