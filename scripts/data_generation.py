import pandas as pd
import json
import os
import random
from datetime import datetime, timedelta

def generate_comprehensive_datasets():
    # --- Step 1: Initialize Folders ---
    # Ensures all folders exist according to the GitHub structure [cite: 342]
    dirs = ["data/raw", "data/processed", "data/synthetic"]
    for d in dirs:
        os.makedirs(f"../{d}", exist_ok=True) # Run from 'scripts' folder

    # --- Step 2: Structured Data (Models & Manufacturers) [cite: 240] ---
    drone_data = [
        {"model": "ideaForge NINJA", "manufacturer": "ideaForge", "class": "Micro", "weight_kg": 2.0, "endurance_min": 25, "price_inr": 450000},
        {"model": "Garuda Kisan Drone", "manufacturer": "Garuda Aerospace", "class": "Small", "weight_kg": 10.0, "endurance_min": 45, "price_inr": 600000},
        {"model": "Agribot", "manufacturer": "IoTechWorld", "class": "Small", "weight_kg": 24.5, "endurance_min": 30, "price_inr": 850000},
        {"model": "Asteria A200", "manufacturer": "Asteria Aerospace", "class": "Micro", "weight_kg": 1.5, "endurance_min": 40, "price_inr": 550000},
        {"model": "Marut AG-365", "manufacturer": "Marut Drones", "class": "Small", "weight_kg": 12.0, "endurance_min": 35, "price_inr": 700000}
    ]
    pd.DataFrame(drone_data).to_csv("../data/processed/drone_models.csv", index=False)

    # --- Step 3: Startup Ecosystem & Training Centers [cite: 243, 244] ---
    companies = [{"name": "ideaForge", "hq": "Mumbai"}, {"name": "Skye Air", "hq": "Delhi"}]
    pd.DataFrame(companies).to_csv("../data/processed/drone_companies.csv", index=False)
    
    rpto = [{"name": "IGRUA", "location": "Amethi"}, {"name": "DroneAcharya", "location": "Pune"}]
    pd.DataFrame(rpto).to_csv("../data/processed/training_institutes.csv", index=False)

    # --- Step 4: Regulation Database (Rules & Penalties) [cite: 241] ---
    reg_db = {
        "rules": [
            {"id": "R1", "title": "UIN Requirement", "desc": "Mandatory for drones >250g"},
            {"id": "R2", "title": "No-Fly Zones", "desc": "Check Digital Sky map for Red Zones"}
        ],
        "penalties": [{"offence": "Flying in Red Zone", "fine": 100000}]
    }
    with open("../data/processed/regulations.json", "w") as f:
        json.dump(reg_db, f, indent=4)

    # --- Step 5: Synthetic Flight Logs (1000 entries) [cite: 251] ---
    flight_logs = []
    for i in range(1000):
        flight_logs.append({
            "flight_id": f"IND-FL-{i:04}",
            "altitude_ft": random.randint(5, 450), # Some violations for testing
            "battery_drain_%": round(random.uniform(10, 80), 2),
            "zone": random.choice(["Green", "Green", "Yellow", "Red"]),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 10000))).strftime("%Y-%m-%d %H:%M")
        })
    pd.DataFrame(flight_logs).to_csv("../data/synthetic/flight_logs.csv", index=False)

    # --- Step 6: ROI Business Scenarios [cite: 242, 252] ---
    roi_scenarios = []
    for i in range(100):
        inv = random.randint(500000, 1500000)
        roi_scenarios.append({
            "scn_id": f"ROI-{i}",
            "investment": inv,
            "daily_revenue": random.randint(5000, 12000),
            "break_even_days": random.randint(150, 400)
        })
    pd.DataFrame(roi_scenarios).to_csv("../data/synthetic/roi_scenarios.csv", index=False)

    print("✅ Comprehensive Datasets Created Successfully!")

if __name__ == "__main__":
    generate_comprehensive_datasets()