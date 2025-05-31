# Fetch data from PTV API
#   fetch_departures.py

import os
import pandas as pd
from datetime import datetime
from utils.ptv_api import fetch_ptv_data

# === Config ===
ROUTE_TYPE = 0      # 0 = Train
ROUTE_ID = 1        # Replace with your line's ID
STOP_ID = 1071      # Replace with your stop ID (e.g., Flinders Street)
DIRECTION_ID = 1    # 0 or 1, depending on direction
OUTPUT_FILE = "data/raw/train_departures_log.csv"

def extract_departure_data(json_data):
    records = []
    for dep in json_data.get("departures", []):
        scheduled = dep.get("scheduled_departure_utc")
        estimated = dep.get("estimated_departure_utc")
        delay = None

        if scheduled and estimated:
            scheduled_dt = datetime.strptime(scheduled, "%Y-%m-%dT%H:%M:%SZ")
            estimated_dt = datetime.strptime(estimated, "%Y-%m-%dT%H:%M:%SZ")
            delay = (estimated_dt - scheduled_dt).total_seconds() / 60

        records.append({
            "timestamp_collected": datetime.utcnow().isoformat(),
            "route_id": dep.get("route_id"),
            "stop_id": dep.get("stop_id"),
            "direction_id": dep.get("direction_id"),
            "platform_number": dep.get("platform_number"),
            "scheduled_departure": scheduled,
            "estimated_departure": estimated,
            "delay_minutes": delay,
            "run_id": dep.get("run_id"),
        })
    return records

def save_to_csv(data, output_path):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)
    print(f"✅ Appended {len(df)} records to {output_path}")

def main():
    print("🔄 Fetching train departures...")
    endpoint = f"/v3/departures/route_type/{ROUTE_TYPE}/stop/{STOP_ID}/route/{ROUTE_ID}"
    params = {
        "direction_id": DIRECTION_ID,
        "max_results": 10,
        "expand": "run"
    }

    try:
        response_json = fetch_ptv_data(endpoint, params)
        records = extract_departure_data(response_json)
        if records:
            save_to_csv(records, OUTPUT_FILE)
        else:
            print("⚠️ No records returned.")
    except Exception as e:
        print(f"❌ Error fetching data: {e}")

if __name__ == "__main__":
    main()
