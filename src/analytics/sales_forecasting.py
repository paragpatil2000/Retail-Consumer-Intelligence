import sqlite3
import os
import pandas as pd
import numpy as np

from sklearn.ensemble import (
    RandomForestRegressor,
    HistGradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# CONFIG
# ============================================================

DB_PATH = "data/retail_consumer.db"
OUTPUT_PATH = "data/processed/sales_forecast.csv"

os.makedirs(
    "data/processed",
    exist_ok=True
)


# ============================================================
# 1. LOAD DATA
# ============================================================

conn = sqlite3.connect(DB_PATH)

sales_query = """
SELECT
    t.transaction_date AS date,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.total_amount
            ELSE 0
        END
    ) AS sales,

    SUM(
        CASE
            WHEN t.return_flag = 0
            THEN t.quantity
            ELSE 0
        END
    ) AS units,

    COUNT(
        CASE
            WHEN t.return_flag = 0
            THEN t.transaction_id
        END
    ) AS transaction_count

FROM transactions t

GROUP BY t.transaction_date

ORDER BY t.transaction_date
"""

daily_sales = pd.read_sql_query(
    sales_query,
    conn
)


calendar_query = """
SELECT
    date,
    year,
    quarter,
    month,
    month_name,
    week_number,
    day,
    day_name,
    day_of_week,
    is_weekend,
    season,
    festival
FROM calendar
"""

calendar = pd.read_sql_query(
    calendar_query,
    conn
)

conn.close()


# ============================================================
# 2. DATE CONVERSION
# ============================================================

daily_sales["date"] = pd.to_datetime(
    daily_sales["date"]
)

calendar["date"] = pd.to_datetime(
    calendar["date"]
)


# ============================================================
# 3. MERGE
# ============================================================

df = daily_sales.merge(
    calendar,
    on="date",
    how="left"
)

df = (
    df
    .sort_values("date")
    .reset_index(drop=True)
)


print("=" * 65)
print("SALES FORECASTING V3")
print("=" * 65)

print(
    f"Total days: {len(df)}"
)

print(
    f"Date range: "
    f"{df['date'].min().date()} "
    f"to "
    f"{df['date'].max().date()}"
)


# ============================================================
# 4. CALENDAR FEATURES
# ============================================================

# Q1, Q2, Q3, Q4 -> 1, 2, 3, 4

df["quarter"] = (
    df["quarter"]
    .astype(str)
    .str.extract(
        r"(\d+)",
        expand=False
    )
    .astype(float)
    .fillna(0)
    .astype(int)
)


# Weekend

df["is_weekend"] = (
    pd.to_numeric(
        df["is_weekend"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)


# Festival flag

df["is_festival"] = (
    df["festival"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
    .astype(int)
)


# ============================================================
# 5. SEASON ENCODING
# ============================================================

season_dummies = pd.get_dummies(
    df["season"].fillna("Unknown"),
    prefix="season",
    dtype=int
)


# ============================================================
# 6. FESTIVAL ENCODING
# ============================================================

festival_dummies = pd.get_dummies(
    df["festival"].fillna("None"),
    prefix="festival",
    dtype=int
)


df = pd.concat(
    [
        df,
        season_dummies,
        festival_dummies
    ],
    axis=1
)


# ============================================================
# 7. LAG FEATURES
# ============================================================

df["sales_lag_1"] = (
    df["sales"].shift(1)
)

df["sales_lag_7"] = (
    df["sales"].shift(7)
)

df["sales_lag_14"] = (
    df["sales"].shift(14)
)

df["sales_lag_30"] = (
    df["sales"].shift(30)
)

df["sales_lag_60"] = (
    df["sales"].shift(60)
)


# Units

df["units_lag_7"] = (
    df["units"].shift(7)
)

df["units_lag_30"] = (
    df["units"].shift(30)
)


# Transactions

df["transactions_lag_7"] = (
    df["transaction_count"].shift(7)
)

df["transactions_lag_30"] = (
    df["transaction_count"].shift(30)
)


# ============================================================
# 8. ROLLING FEATURES
# ============================================================

df["sales_rolling_7"] = (
    df["sales"]
    .shift(1)
    .rolling(7)
    .mean()
)

df["sales_rolling_14"] = (
    df["sales"]
    .shift(1)
    .rolling(14)
    .mean()
)

df["sales_rolling_30"] = (
    df["sales"]
    .shift(1)
    .rolling(30)
    .mean()
)

df["sales_std_7"] = (
    df["sales"]
    .shift(1)
    .rolling(7)
    .std()
)

df["sales_std_30"] = (
    df["sales"]
    .shift(1)
    .rolling(30)
    .std()
)


# ============================================================
# 9. SALES MOMENTUM FEATURES
# ============================================================

df["sales_growth_7"] = (
    df["sales_lag_1"]
    /
    df["sales_lag_7"]
    - 1
)

df["sales_growth_30"] = (
    df["sales_lag_1"]
    /
    df["sales_lag_30"]
    - 1
)


# Replace infinity

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)


# ============================================================
# 10. TREND
# ============================================================

df["trend"] = np.arange(
    len(df)
)


# ============================================================
# 11. FEATURE LIST
# ============================================================

feature_columns = [

    # Calendar
    "year",
    "quarter",
    "month",
    "week_number",
    "day",
    "day_of_week",
    "is_weekend",
    "is_festival",

    # Sales lag
    "sales_lag_1",
    "sales_lag_7",
    "sales_lag_14",
    "sales_lag_30",
    "sales_lag_60",

    # Units
    "units_lag_7",
    "units_lag_30",

    # Transactions
    "transactions_lag_7",
    "transactions_lag_30",

    # Rolling
    "sales_rolling_7",
    "sales_rolling_14",
    "sales_rolling_30",

    "sales_std_7",
    "sales_std_30",

    # Momentum
    "sales_growth_7",
    "sales_growth_30",

    # Trend
    "trend"
]


feature_columns.extend(
    list(season_dummies.columns)
)

feature_columns.extend(
    list(festival_dummies.columns)
)


print()
print("=" * 65)
print("FEATURE ENGINEERING")
print("=" * 65)

print(
    f"Total features: {len(feature_columns)}"
)


# ============================================================
# 12. NUMERIC CONVERSION
# ============================================================

for column in feature_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# 13. REMOVE MISSING VALUES
# ============================================================

model_df = df.dropna(
    subset=feature_columns
).copy()

model_df = (
    model_df
    .reset_index(drop=True)
)


# ============================================================
# 14. X AND Y
# ============================================================

X = model_df[
    feature_columns
]

y = model_df[
    "sales"
]


# ============================================================
# 15. TIME-BASED SPLIT
# ============================================================

split_index = int(
    len(model_df) * 0.80
)


X_train = X.iloc[
    :split_index
]

X_test = X.iloc[
    split_index:
]


y_train = y.iloc[
    :split_index
]

y_test = y.iloc[
    split_index:
]


test_dates = model_df[
    "date"
].iloc[
    split_index:
]


print()
print("=" * 65)
print("TRAIN TEST SPLIT")
print("=" * 65)

print(
    f"Training records: {len(X_train)}"
)

print(
    f"Testing records: {len(X_test)}"
)


# ============================================================
# 16. BASELINE
# ============================================================

baseline_predictions = X_test[
    "sales_lag_7"
]


baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        baseline_predictions
    )
)

baseline_r2 = r2_score(
    y_test,
    baseline_predictions
)


# ============================================================
# 17. RANDOM FOREST
# ============================================================

print()
print("=" * 65)
print("TRAINING RANDOM FOREST")
print("=" * 65)


rf_model = RandomForestRegressor(

    n_estimators=300,

    max_depth=18,

    min_samples_leaf=2,

    random_state=42,

    n_jobs=-1
)


rf_model.fit(
    X_train,
    y_train
)


rf_predictions = rf_model.predict(
    X_test
)


rf_mae = mean_absolute_error(
    y_test,
    rf_predictions
)

rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        rf_predictions
    )
)

rf_r2 = r2_score(
    y_test,
    rf_predictions
)


# ============================================================
# 18. HISTOGRAM GRADIENT BOOSTING
# ============================================================

print()
print("=" * 65)
print("TRAINING HISTOGRAM GRADIENT BOOSTING")
print("=" * 65)


hgb_model = HistGradientBoostingRegressor(

    max_iter=300,

    learning_rate=0.05,

    max_leaf_nodes=15,

    l2_regularization=1.0,

    random_state=42
)


hgb_model.fit(
    X_train,
    y_train
)


hgb_predictions = hgb_model.predict(
    X_test
)


hgb_mae = mean_absolute_error(
    y_test,
    hgb_predictions
)

hgb_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        hgb_predictions
    )
)

hgb_r2 = r2_score(
    y_test,
    hgb_predictions
)


# ============================================================
# 19. MODEL COMPARISON
# ============================================================

comparison_df = pd.DataFrame({

    "model": [
        "7-Day Baseline",
        "Random Forest",
        "HistGradientBoosting"
    ],

    "MAE": [
        baseline_mae,
        rf_mae,
        hgb_mae
    ],

    "RMSE": [
        baseline_rmse,
        rf_rmse,
        hgb_rmse
    ],

    "R2": [
        baseline_r2,
        rf_r2,
        hgb_r2
    ]
})


# Sort by MAE

comparison_df = (
    comparison_df
    .sort_values("MAE")
    .reset_index(drop=True)
)


print()
print("=" * 65)
print("MODEL COMPARISON")
print("=" * 65)

print(
    comparison_df.to_string(
        index=False
    )
)


# ============================================================
# 20. SELECT BEST MODEL
# ============================================================

best_model_name = comparison_df.iloc[
    0
]["model"]


if best_model_name == "7-Day Baseline":

    best_predictions = baseline_predictions

elif best_model_name == "Random Forest":

    best_predictions = rf_predictions

else:

    best_predictions = hgb_predictions


print()
print(
    f"Selected model: {best_model_name}"
)


# ============================================================
# 21. FEATURE IMPORTANCE
# ============================================================

if best_model_name == "Random Forest":

    importance_df = pd.DataFrame({

        "feature":
            feature_columns,

        "importance":
            rf_model.feature_importances_

    })

    importance_df = (
        importance_df
        .sort_values(
            "importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print()
    print("=" * 65)
    print("TOP FEATURES")
    print("=" * 65)

    print(
        importance_df
        .head(15)
        .to_string(index=False)
    )


elif best_model_name == "HistGradientBoosting":

    print()
    print(
        "HistGradientBoosting selected."
    )

    print(
        "Feature importance is not displayed "
        "because this estimator does not provide "
        "feature_importances_ directly."
    )


# ============================================================
# 22. FORECAST OUTPUT
# ============================================================

forecast_df = pd.DataFrame({

    "date":
        test_dates.values,

    "actual_sales":
        y_test.values,

    "baseline_prediction":
        baseline_predictions.values,

    "random_forest_prediction":
        rf_predictions,

    "gradient_boosting_prediction":
        hgb_predictions,

    "forecast_sales":
        best_predictions

})


# ============================================================
# 23. ERROR CALCULATION
# ============================================================

forecast_df["forecast_error"] = (

    forecast_df["actual_sales"]

    -

    forecast_df["forecast_sales"]

)


forecast_df["absolute_error"] = (

    forecast_df["forecast_error"]
    .abs()

)


forecast_df["percentage_error"] = np.where(

    forecast_df["actual_sales"] != 0,

    (
        forecast_df["absolute_error"]
        /
        forecast_df["actual_sales"]
    ) * 100,

    0

)


# ============================================================
# 24. SAVE FORECAST
# ============================================================

forecast_df.to_csv(

    OUTPUT_PATH,

    index=False

)


# ============================================================
# 25. FORECAST SAMPLE
# ============================================================

print()
print("=" * 65)
print("FORECAST SAMPLE")
print("=" * 65)

print(
    forecast_df
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 26. FINAL SUMMARY
# ============================================================

best_row = comparison_df.iloc[0]


print()
print("=" * 65)
print("FINAL FORECASTING SUMMARY")
print("=" * 65)

print(
    f"Best Model : {best_model_name}"
)

print(
    f"MAE        : ₹{best_row['MAE']:,.2f}"
)

print(
    f"RMSE       : ₹{best_row['RMSE']:,.2f}"
)

print(
    f"R²         : {best_row['R2']:.4f}"
)

print(
    f"Forecast Rows: {len(forecast_df)}"
)

print(
    f"Output: {OUTPUT_PATH}"
)

print("=" * 65)

print(
    "SALES FORECASTING V3 COMPLETED"
)

print("=" * 65)