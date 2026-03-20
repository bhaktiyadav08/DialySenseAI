import requests
import random
import time

URL = "http://127.0.0.1:5000/predict"

while True:
    data = {
        "temperature": round(random.uniform(35, 40), 2),
        "flow_rate": round(random.uniform(0.5, 3.0), 2),
        "water_level": round(random.uniform(50, 100), 2)
    }

    try:
        response = requests.post(URL, json=data)
        print("Sent:", data, "Response:", response.json())
    except Exception as e:
        print("Error:", e)

    time.sleep(5)