import pandas as pd
from pathlib import Path

csv_path = Path("dataset/processed/flights_cleaned.csv")
parquet_path = Path("dataset/processed/flights_cleaned.parquet")

print("Loading CSV...")
df = pd.read_csv(csv_path)

print("Optimising datatypes...")

# ---------- integer columns ----------
int_cols = [
    "YEAR", "MONTH", "DAY_OF_WEEK"
]

for col in int_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")

# ---------- float columns ----------
float_cols = [
    "DEP_DELAY_MINUTES",
    "ARR_DELAY_MINUTES",
    "TAXI_OUT",
    "TAXI_IN",
    "ELAPSED_TIME",
    "AIR_TIME",
    "DISTANCE",
    "DELAY_DUE_CARRIER",
    "DELAY_DUE_WEATHER",
    "DELAY_DUE_NAS",
    "DELAY_DUE_SECURITY",
    "DELAY_DUE_LATE_AIRCRAFT"
]

for col in float_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], downcast="float")

# ---------- category columns ----------
category_cols = [
    "AIRLINE",
    "AIRLINE_CODE",
    "ORIGIN",
    "DEST",
    "ORIGIN_CITY",
    "DEST_CITY",
    "PUNCTUALITY_STATUS",
    "DOMINANT_DELAY_CAUSE"
]

for col in category_cols:
    if col in df.columns:
        df[col] = df[col].astype("category")

# ---------- boolean columns ----------
bool_cols = [
    "IS_DELAYED",
    "IS_CANCELLED",
    "IS_DIVERTED"
]

for col in bool_cols:
    if col in df.columns:
        df[col] = df[col].astype("bool")

# ---------- date handling ----------
if "FL_DATE" in df.columns:
    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

print("Writing compressed parquet...")

df.to_parquet(
    parquet_path,
    engine="pyarrow",
    compression="brotli",   # stronger than snappy
    index=False
)

csv_size = csv_path.stat().st_size / (1024 * 1024)
parquet_size = parquet_path.stat().st_size / (1024 * 1024)

print(f"CSV Size: {csv_size:.2f} MB")
print(f"Compressed Parquet Size: {parquet_size:.2f} MB")