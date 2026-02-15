import pandas as pd
import random

def generate_flight_logs(num_records=100):
    data = {
        "drone_id": [f"DR-{i:03d}" for i in range(num_records)],
        "flight_time_min": [random.randint(10, 45) for _ in range(num_records)],
        "battery_cycles": [random.randint(1, 200) for _ in range(num_records)]
    }
    df = pd.DataFrame(data)
    df.to_csv("data/synthetic/flight_logs.csv", index=False)
    print("Synthetic flight logs generated.")

if __name__ == "__main__":
    generate_flight_logs()