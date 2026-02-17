def check_regulation_compliance(weight_kg: float, zone: str, altitude_ft: float, purpose: str = "Recreational"):
    violations = []
    permits = []
    status = "Compliant"

    # Zone Analysis
    zone = zone.lower()
    if zone == "red":
        violations.append("Flight strictly prohibited in Red Zone.")
        status = "Non-Compliant"
    elif zone == "yellow":
        permits.append("ATC Permission required (Yellow Zone).")
        status = "Conditional"
    elif zone == "green":
        if altitude_ft > 400:
            violations.append("Altitude exceeds 400ft limit for Green Zone.")
            status = "Non-Compliant"

    # Weight Category Analysis
    if weight_kg > 0.25:
        permits.append("UIN (Unique Identification Number) Registration")
    
    if weight_kg > 2 or purpose.lower() == "commercial":
        permits.append("Remote Pilot Certificate (RPC)")
        permits.append("Third-party Insurance")

    return {
        "status": status,
        "violations": violations,
        "required_permits": permits,
        "zone_info": f"{zone.title()} Zone rules apply."
    }