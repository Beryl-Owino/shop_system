from shop_db import add_sale, get_sales, get_mpesa_transactions
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# FUNCTION: SHOW REPORT
# ==============================
def show_report():
    rows = get_sales()

    report_data = []
    total_revenue = 0
    total_cost = 0

    for id, item, variant, qty, price, cost, date in rows:
        revenue = qty * price
        item_cost = qty * cost
        profit = revenue - item_cost

        total_revenue += revenue
        total_cost += item_cost

        report_data.append({
            "id": id,
            "item": item,
            "variant": variant,
            "qty": qty,
            "revenue": revenue,
            "cost": item_cost,
            "profit": profit,
            "date": date
        })

    total_profit = total_revenue - total_cost

    return report_data, total_revenue, total_cost, total_profit

# ==============================
# FUNCTION: DAILY SALES SUMMARY
# ==============================
def daily_sales_summary():
    rows = get_sales()
    daily_totals = defaultdict(int)

    for id, item, variant, qty, price, cost, date in rows:
        day = date.split(" ")[0]
        daily_totals[day] += qty * price

    return dict(daily_totals)


# ==============================
# FUNCTION: SMART INSIGHTS
# ==============================
def smart_insights():
    rows = get_sales()

    item_profit = defaultdict(int)
    daily_revenue = defaultdict(int)
    total_profit = 0

    for id, item, variant, qty, price, cost, date in rows:
        revenue = qty * price
        profit = revenue - (qty * cost)

        day = date.split(" ")[0]
        name = f"{item}-{variant}"

        item_profit[name] += profit
        daily_revenue[day] += revenue
        total_profit += profit

    if not item_profit:
        return None

    return {
        "total_profit": total_profit,
        "best_item": max(item_profit, key=item_profit.get),
        "worst_item": min(item_profit, key=item_profit.get),
        "best_day": max(daily_revenue, key=daily_revenue.get),
        "worst_day": min(daily_revenue, key=daily_revenue.get),
    }


# ==============================
# FUNCTION: M-PESA DAILY SUMMARY
# ==============================
def mpesa_daily_summary():
    rows = get_mpesa_transactions()
    daily_totals = defaultdict(int)

    for id, date, description, amount, balance, category in rows:
        if category == "income":
            day = date.split(" ")[0]
            daily_totals[day] += amount

    return dict(daily_totals)


# ==============================
# FUNCTION: M-PESA PEAK HOURS
# ==============================
def mpesa_peak_hours():
    rows = get_mpesa_transactions()
    hourly_totals = defaultdict(int)

    for _, date, _, amount, _, category in rows:
        if category == "income":
            hour = date.split(" ")[1].split(":")[0]
            hourly_totals[hour] += amount

    return dict(hourly_totals)


# ==============================
# FUNCTION: TOTAL BUSINESS SUMMARY
# ==============================
def total_business_summary():
    sales_rows = get_sales()
    mpesa_rows = get_mpesa_transactions()

    total_sales = sum(qty * price for _, _, _, qty, price, _, _ in sales_rows)

    total_mpesa = sum(
        amount for _, _, _, amount, _, category in mpesa_rows
        if category == "income"
    )

    return {
        "sales": total_sales,
        "mpesa": total_mpesa,
        "total": total_sales + total_mpesa
    }


# ==============================
# FUNCTION: GAP ANALYSIS
# ==============================
def income_gap_analysis():
    sales_rows = get_sales()
    mpesa_rows = get_mpesa_transactions()

    total_sales = sum(qty * price for _, _, _, qty, price, _, _ in sales_rows)

    total_mpesa = sum(
        amount for _, _, _, amount, _, category in mpesa_rows
        if category == "income"
    )

    return {
        "sales": total_sales,
        "mpesa": total_mpesa,
        "gap": total_sales - total_mpesa
    }


# ==============================
# OPTIONAL: EXPORT TO EXCEL
# ==============================
def export_to_excel():
    rows = get_sales()

    df = pd.DataFrame(rows, columns=["Item", "Variant", "Qty", "Price", "Cost", "Date"])

    df["Revenue"] = df["Qty"] * df["Price"]
    df["Cost Total"] = df["Qty"] * df["Cost"]
    df["Profit"] = df["Revenue"] - df["Cost Total"]

    df.to_excel("sales_report.xlsx", index=False)

    return "sales_report.xlsx"