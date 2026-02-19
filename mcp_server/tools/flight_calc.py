def get_flight_estimates(battery_ah: float, drone_weight: float, payload: float, wind_condition: str = "Calm"):
    total_mass = drone_weight + payload
    # Flight time formula adjusted for standard Indian drone efficiency
    base_minutes = (battery_ah * 14) / (total_mass * 0.5)
    
    # Wind factor Adjustment
    wind_factor = 1.0
    if wind_condition.lower() == "moderate":
        wind_factor = 0.85
    elif wind_condition.lower() == "high wind":
        wind_factor = 0.60
        
    minutes = base_minutes * wind_factor
    
    return {
        "estimated_minutes": round(minutes, 2),
        "safe_minutes": round(minutes * 0.8, 2),  # 20% safety margin
        "range_km": round((minutes / 60) * 45, 2)
    }