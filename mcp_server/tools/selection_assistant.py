import pandas as pd
import os

def recommend_drone(max_budget: float, primary_use: str):
    """
    Filters the drone_models.csv to find the best match.
    """
    # Use absolute path for robustness
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_path, "data", "processed", "drone_models.csv")
    
    if not os.path.exists(csv_path):
        return {"error": "Drone database not found. Please run data_generation.py"}

    try:
        df = pd.read_csv(csv_path)
        
        # Filter by budget
        affordable_drones = df[df['price_inr'] <= max_budget]
        
        if affordable_drones.empty:
            return {"message": "No drones found within this budget. Try increasing your range."}

        # Simple logic to match use-case to drone class
        if "agri" in primary_use.lower():
            recommendation = affordable_drones[affordable_drones['class'] == 'Small'].head(3)
        else:
            recommendation = affordable_drones.sort_values(by='endurance_min', ascending=False).head(3)

        return recommendation.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}