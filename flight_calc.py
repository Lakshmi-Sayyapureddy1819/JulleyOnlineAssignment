def calculate_flight_time(battery_capacity_mah: float, voltage: float, power_consumption_watts: float) -> float:
    """
    Calculate estimated flight time in minutes.
    """
    battery_energy_wh = (battery_capacity_mah / 1000) * voltage
    flight_time_hours = battery_energy_wh / power_consumption_watts
    return flight_time_hours * 60

def estimate_range(flight_time_min: float, avg_speed_kmh: float) -> float:
    """
    Calculate estimated range in kilometers.
    """
    return (avg_speed_kmh * (flight_time_min / 60))