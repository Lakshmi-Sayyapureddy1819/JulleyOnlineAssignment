def get_flight_estimates(battery_ah: float, drone_weight: float, payload: float):
    total_mass = drone_weight + payload
    # Flight time formula adjusted for standard Indian drone efficiency
    minutes = (battery_ah * 14) / (total_mass * 0.5)
    return {
        "estimated_minutes": round(minutes, 2),
        "safe_minutes": round(minutes * 0.8, 2),  # 20% safety margin
        "range_km": round((minutes / 60) * 45, 2)
    }