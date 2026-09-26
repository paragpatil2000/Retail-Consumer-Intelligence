import os
import pandas as pd


# ---------------------------------------------------------
# 1. SETTINGS
# ---------------------------------------------------------

START_DATE = "2024-01-01"
END_DATE = "2026-12-31"

OUTPUT_PATH = "data/raw/calendar.csv"


# ---------------------------------------------------------
# 2. CREATE DATE RANGE
# ---------------------------------------------------------

dates = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)


# ---------------------------------------------------------
# 3. CREATE CALENDAR DATA
# ---------------------------------------------------------

calendar = pd.DataFrame({
    "date": dates
})

calendar["date_key"] = (
    calendar["date"].dt.strftime("%Y%m%d").astype(int)
)

calendar["year"] = calendar["date"].dt.year

calendar["quarter"] = (
    "Q" + calendar["date"].dt.quarter.astype(str)
)

calendar["month"] = calendar["date"].dt.month

calendar["month_name"] = (
    calendar["date"].dt.month_name()
)

calendar["week_number"] = (
    calendar["date"].dt.isocalendar().week.astype(int)
)

calendar["day"] = calendar["date"].dt.day

calendar["day_name"] = (
    calendar["date"].dt.day_name()
)

calendar["day_of_week"] = (
    calendar["date"].dt.dayofweek + 1
)

calendar["is_weekend"] = (
    calendar["date"].dt.dayofweek >= 5
)


# ---------------------------------------------------------
# 4. FINANCIAL YEAR
# ---------------------------------------------------------

calendar["financial_year"] = (
    calendar["year"].astype(str)
    + "-"
    + (calendar["year"] + 1).astype(str)
)


# ---------------------------------------------------------
# 5. SEASON
# ---------------------------------------------------------

def get_season(month):

    if month in [3, 4, 5]:
        return "Summer"

    elif month in [6, 7, 8, 9]:
        return "Monsoon"

    elif month in [10, 11]:
        return "Festive"

    else:
        return "Winter"


calendar["season"] = calendar["month"].apply(
    get_season
)


# ---------------------------------------------------------
# 6. FESTIVAL
# ---------------------------------------------------------

def get_festival(month, day):

    if month == 1 and day == 1:
        return "New Year"

    elif month == 1 and day == 26:
        return "Republic Day"

    elif month == 8 and day == 15:
        return "Independence Day"

    elif month == 12 and day == 25:
        return "Christmas"

    else:
        return "None"


calendar["festival"] = calendar.apply(
    lambda row: get_festival(
        row["month"],
        row["day"]
    ),
    axis=1
)


# ---------------------------------------------------------
# 7. SAVE
# ---------------------------------------------------------

os.makedirs("data/raw", exist_ok=True)

calendar.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------------------------
# 8. OUTPUT
# ---------------------------------------------------------

print("Calendar generated successfully!")
print(f"Total dates: {len(calendar):,}")
print(f"Saved to: {OUTPUT_PATH}")