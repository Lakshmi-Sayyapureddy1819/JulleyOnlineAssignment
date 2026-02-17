def get_roi_analysis(investment: float, daily_revenue: float):
    daily_op_cost = 2500  # Avg pilot + battery charging + maintenance
    daily_profit = daily_revenue - daily_op_cost
    break_even = investment / daily_profit if daily_profit > 0 else 0
    return {
        "net_daily_profit": daily_profit,
        "break_even_days": round(break_even),
        "status": "Profitable" if daily_profit > 0 else "Review Pricing"
    }