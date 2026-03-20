import csv
import random

def generate_data(n=1000):
    data = []

    for _ in range(n):
        # Random normal values
        temp = round(random.uniform(35, 40), 2)
        flow = round(random.uniform(1.0, 2.5), 2)
        level = round(random.uniform(60, 80), 2)

        # Logic for labeling
        if flow < 1.5:
            status = "blockage"
        else:
            status = "normal"

        data.append([temp, flow, level, status])

    return data


def save_to_csv(data):
    with open("../data/raw/dataset.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature", "flow_rate", "water_level", "status"])
        writer.writerows(data)


if __name__ == "__main__":
    dataset = generate_data(1000)
    save_to_csv(dataset)
    print("Dataset generated successfully!")