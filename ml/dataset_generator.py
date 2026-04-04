import csv
import random
import os
def generate_data(n=5000): # Increased n for better accuracy
    data = []
    for _ in range(n):
        # 1. Generate realistic sensor ranges
        temp = round(random.uniform(20.0, 45.0), 2)
        flow = round(random.uniform(0.0, 1500.0), 2)
        # Note: 'distance' in ESP is the water level
        level = round(random.uniform(2.0, 15.0), 2) 

        # 2. MATCH YOUR ESP LOGIC EXACTLY
        status = "normal"
        
        # Temp Threshold (TEMP_THRESHOLD 35.0)
        if temp > 35.0:
            status = "blockage"
        
        # Level Logic (LEVEL_OFF 5.0)
        if level <= 5.0:
            status = "blockage"
            
        # Flow Logic (300-600 and > 1244.44)
        if (flow >= 300 and flow < 600) or (flow > 1244.44):
            status = "blockage"

        data.append([temp, flow, level, status])
    return data


def save_to_csv(data):
    # 1. Get the directory of THIS script (dataset_generator.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Path: from 'ml' folder, go up one level, then into 'data/raw'
    csv_path = os.path.normpath(os.path.join(current_dir, "..", "data", "raw", "dataset.csv"))

    # 3. Create the folders if they don't exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    # 4. Open and write data
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Write Header
            writer.writerow(["temperature", "flow_rate", "water_level", "status"])
            # Write Data - Ensure 'data' is a list of lists
            if data:
                writer.writerows(data)
                f.flush() # Forces the data to be written to disk
            else:
                print("Warning: The 'data' variable is empty!")
        
        print(f"✅ SUCCESS: Saved {len(data)} rows to {csv_path}")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}")

if __name__ == "__main__":
    # Ensure your generate_data function actually returns a list!
    dataset = generate_data(5000) 
    save_to_csv(dataset)