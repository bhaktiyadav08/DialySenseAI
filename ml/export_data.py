"""
export_data.py
--------------
Run this after collecting real sensor data at college.
Exports MongoDB sensor_data collection to a CSV for retraining.

Usage:
    python export_data.py
    python export_data.py --limit 500        # export last 500 records
    python export_data.py --out my_data.csv  # custom filename
"""

import argparse
import csv
import os
from pymongo import MongoClient
from datetime import datetime

# ── Args ──────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=0,    help='Max records to export (0 = all)')
parser.add_argument('--out',   type=str, default='',   help='Output CSV filename')
args = parser.parse_args()

# ── Connect ───────────────────────────────────────────────────────────────────
client     = MongoClient("mongodb://localhost:27017/")
db         = client["dialysense"]
collection = db["sensor_data"]

# ── Query ─────────────────────────────────────────────────────────────────────
query  = collection.find().sort("timestamp", 1)   # oldest first
if args.limit > 0:
    query = query.limit(args.limit)

records = list(query)

if not records:
    print("No records found in MongoDB. Make sure Flask has been running and collecting data.")
    exit(1)

# ── Output path ───────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
RAW_DIR   = os.path.join(BASE_DIR, 'data', 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
filename  = args.out if args.out else f"real_sensor_data_{timestamp_str}.csv"
out_path  = os.path.join(RAW_DIR, filename)

# ── Write CSV ─────────────────────────────────────────────────────────────────
# These columns must match what training.py expects as features
FIELDS = ['temperature', 'flow_rate', 'water_level', 'status', 'timestamp']

normal_count = 0
fault_count  = 0

with open(out_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()

    for r in records:
        status = r.get('status', 'normal')
        if status == 'normal':
            normal_count += 1
        else:
            fault_count += 1

        writer.writerow({
            'temperature': round(float(r.get('temperature', 0)), 3),
            'flow_rate':   round(float(r.get('flow_rate',   0)), 3),
            'water_level': round(float(r.get('water_level', 0)), 3),
            'status':      status,
            'timestamp':   r.get('timestamp', ''),
        })

# ── Summary ───────────────────────────────────────────────────────────────────
total = normal_count + fault_count
print(f"\n✅ Exported {total} records → {out_path}")
print(f"   Normal  : {normal_count} ({round(normal_count/total*100,1)}%)")
print(f"   Fault   : {fault_count}  ({round(fault_count/total*100,1)}%)")
print(f"\nNext step: update the filename in training.py and run:")
print(f"   python ml/training.py --data data/raw/{filename}")