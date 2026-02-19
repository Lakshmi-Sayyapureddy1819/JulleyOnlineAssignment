def get_roi_analysis(investment: float, daily_revenue: float, operational_costs: float = 2500, use_case: str = "General"):
    # operational_costs is now a parameter (default 2500 if not provided)
    # Convert monthly op costs to daily if needed, but here we assume the input might be daily or monthly.
    # The requirement says "Operational Costs (Maintenance, Insurance, Pilot Salary per month)".
    # If the input is monthly, we should divide by 30.
    # Let's assume the input `operational_costs` is MONTHLY based on the prompt description "Pilot Salary per month".
    
    daily_op_cost = operational_costs / 30
    daily_profit = daily_revenue - daily_op_cost
    
    break_even = investment / daily_profit if daily_profit > 0 else 0
    
    status = "Profitable"
    if daily_profit <= 0:
        status = "Loss Making"
    elif break_even > 730: # > 2 years
        status = "Long-term Return"
        
    return {
        "net_daily_profit": round(daily_profit, 2),
        "break_even_days": round(break_even),
        "status": status,
        "use_case_analyzed": use_case
    }