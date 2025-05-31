# scripts/preprocess_data.py

import pandas as pd
from datetime import datetime
import os

RAW_FILE = "data/raw/train_departures_log.csv"
CLEAN_FILE = "data/processed/train_clean.csv"

def preprocess_train_data(raw_path, save_path):
    df = pd.read_csv(raw_path)

    # Drop rows missing essential time info
    df.dropna(subset=["scheduled_departure"], inplace=True)

    # Parse UTC timestamps into datetime
    df["scheduled_dt"] = pd.to_datetime(df["scheduled_departure"], utc=True, errors="coerce")
    df["timestamp_dt"] = pd.to_datetime(df["timestamp_collected"], utc=True, errors="coerce")

    # Feature: Hour of day & Day of week
    df["hour"] = df["scheduled_dt"].dt.hour
    df["weekday"] = df["scheduled_dt"].dt.weekday  # Monday = 0

    # Target: Delayed (binary classification)
    df["is_delayed"] = df["delay_minutes"].fillna(0).apply(lambda x: 1 if x > 3 else 0)

    # Drop unused fields
    df = df.drop(columns=["platform_number", "run_id"])

    # Save processed data
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"✅ Cleaned data saved to {save_path}. Rows: {len(df)}")

if __name__ == "__main__":
    preprocess_train_data(RAW_FILE, CLEAN_FILE)
