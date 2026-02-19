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
    if weight_kg <= 0.25:
        category = "Nano"
    elif weight_kg <= 2.0:
        category = "Micro"
    elif weight_kg <= 25.0:
        category = "Small"
    elif weight_kg <= 150.0:
        category = "Medium"
    else:
        category = "Large"

    # Nano drones (<= 250g) are exempt from UIN and RPC if recreational
    if category != "Nano":
        permits.append("UIN (Unique Identification Number) Registration")
    
    # Commercial use ALWAYS requires RPC, regardless of weight (mostly)
    # But strictly speaking, Nano non-commercial is exempt. 
    # Micro and above need RPC.
    
    if purpose.lower() == "commercial":
         permits.append("Remote Pilot Certificate (RPC)")
         permits.append("Third-party Insurance")
         if category == "Nano":
              permits.append("Nano Commercial Operations requires Flight Log") # Just a specific note
    elif category != "Nano":
         # Recreational but > Nano still typically needs some training/awareness, but RPC is main commercialreq.
         # Actually Micro+ needs RPC even for recreational in many interpretations, but let's stick to simple logic:
         if weight_kg > 2.0: 
             permits.append("Remote Pilot Certificate (RPC)") # Required for Small+ even if recreational usually

    return {
        "status": status,
        "violations": violations,
        "required_permits": permits,
        "zone_info": f"{zone.title()} Zone rules apply."
    }