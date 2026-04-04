import requests
import random
import time

URL = "http://127.0.0.1:5000/predict"

while True:
    # 50% chance to generate a "Normal" state vs a "Faulty" state
    is_faulty = random.choice([True, False])

    if not is_faulty:
        # NORMAL VALUES (Matches ESP thresholds)
        data = {
            "temperature": round(random.uniform(25.0, 32.0), 2),
            "flow_rate": round(random.uniform(800.0, 1000.0), 2),
            "water_level": round(random.uniform(15.0, 25.0), 2)
        }
    else:
        # FAULTY VALUES (Triggers HOT, LOW, or FHIGH/FMID)
        # Pick one random type of fault to simulate
        fault_type = random.randint(1, 3)
        if fault_type == 1: # High Temp
            data = {"temperature": 45.0, "flow_rate": 900.0, "water_level": 20.0}
        elif fault_type == 2: # Low Water Level (ESP LEVEL_OFF is 5.0)
            data = {"temperature": 28.0, "flow_rate": 900.0, "water_level": 3.0}
        else: # High Flow (ESP FHIGH is > 1244)
            data = {"temperature": 28.0, "flow_rate": 1300.0, "water_level": 20.0}

    try:
        response = requests.post(URL, json=data)
        # Check if the response contains the predicted status
        print(f"Sent: {data} | Prediction: {response.json().get('status')}")
    except Exception as e:
        print("Error connecting to Flask:", e)

    # Change to 2 seconds to match your dashboard refresh
    time.sleep(2)
