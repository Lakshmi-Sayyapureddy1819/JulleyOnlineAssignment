import pandas as pd
import os

def recommend_drones(budget: float, min_endurance: int):
    # Resolve path to data
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_path, "data", "processed", "drone_models.csv")
    
    if not os.path.exists(data_path):
        return {"error": "Drone database not found. Please run data generation script."}
    
    try:
        df = pd.read_csv(data_path)
        
        # Filter logic
        filtered_df = df[
            (df["price_inr"] <= budget) & 
            (df["endurance_min"] >= min_endurance)
        ]
        
        if filtered_df.empty:
            return {"message": "No drones found within this budget and endurance range.", "count": 0, "models": []}
            
        # Sort by price descending
        results = filtered_df.sort_values(by="price_inr", ascending=False).head(5)
        
        return {
            "count": len(results),
            "models": results.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}