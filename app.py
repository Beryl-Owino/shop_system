import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import os
os.makedirs("uploads", exist_ok=True)
from shop_analyzer import (
    show_report,
    daily_sales_summary,
    smart_insights,
    mpesa_daily_summary,
    mpesa_peak_hours,
    total_business_summary,
    income_gap_analysis
)

app = Flask(__name__)

# =========================
# CREATING HOME DASHBOARD
# =========================

@app.route("/")
def home():
    business = total_business_summary()
    gap_data = income_gap_analysis()
    data = daily_sales_summary()

    days = list(sorted(data.keys()))
    totals = [data[d] for d in days]

    plt.figure()
    plt.plot(days, totals, marker='o')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        "home.html",
        sales=business["sales"],
        mpesa=business["mpesa"],
        total=business["total"],
        gap=gap_data["gap"],
        graph=graph_url
    )
# ==============
# REPORT PAGE
# ==============

@app.route("/report")
def report():
    date_filter = request.args.get("date")
    search = request.args.get("search")

    data, total_revenue, total_cost, total_profit = show_report()

    # FILTER BY DATE
    if date_filter:
        data = [row for row in data if row["date"].startswith(date_filter)]

    # FILTER BY SEARCH
    if search:
        data = [
            row for row in data
            if search.lower() in row["item"].lower()
            or search.lower() in row["variant"].lower()
        ]

    return render_template(
        "report.html",
        data=data,
        total_revenue=total_revenue,
        total_cost=total_cost,
        total_profit=total_profit
    )

# ==============
# DAILY SUMMARY
# ==============

@app.route("/daily")
def daily():
    data = daily_sales_summary()

    return render_template(
        "daily.html",
        title="Daily Summary",
        data=data
    )

# ==============
# SMART INSIGHT
# ==============

@app.route("/insights")
def insights():
    data = smart_insights()

    return render_template(
        "insights.html",
        title="Smart Insights",
        total_profit=data["total_profit"],
        best_item=data["best_item"],
        worst_item=data["worst_item"],
        best_day=data["best_day"],
        worst_day=data["worst_day"]
    )

# ==============
# GAP ANALYSIS
# ==============

@app.route("/gap")
def gap():
    data = income_gap_analysis()

    return render_template(
        "gap.html",
        title="Income Gap Analysis",
        sales=data["sales"],
        mpesa=data["mpesa"],
        gap=data["gap"]
    )

# ==============
# CHARTS
# ==============

@app.route("/chart")
def chart():
    data = daily_sales_summary()

    days = list(sorted(data.keys()))
    totals = [data[day] for day in days]

    plt.figure()
    plt.plot(days, totals, marker='o')
    plt.xticks(rotation=45)
    plt.title("Daily Sales Revenue")

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template(
        "chart.html",
        title="Sales Chart",
        graph=graph_url
    )

#=================
# USER INPUT
#================

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        item = request.form["item"]
        variant = request.form["variant"]
        qty = int(request.form["qty"])
        price = int(request.form["price"])
        cost = int(request.form["cost"])

        from shop_db import add_sale
        add_sale(item, variant, qty, price, cost)

        return redirect(url_for("report"))

    return render_template("add.html")

#=================
# DELETE SALE
#=================
from shop_db import delete_sale

@app.route("/delete/<int:id>")
def delete(id):
    delete_sale(id)
    return redirect("/report")




#=================
# UPLOAD
#=================

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]

        filepath = "uploads/" + file.filename
        file.save(filepath)

        import pandas as pd
        df = pd.read_excel(filepath)

        from shop_db import add_mpesa_transaction

        for _, row in df.iterrows():
            receipt = str(row["receipt"])
            date = str(row["date"])
            t_type = str(row["type"])
            amount = float(row["amount"])
            balance = float(row["balance"])
            category = str(row["category"]).lower()

            add_mpesa_transaction(
                receipt, date, t_type, amount, balance, category
            )

        return "✅ M-Pesa data uploaded and saved successfully!"

    return render_template("upload.html")

#=========================
# RUN THE APP
#=========================

if __name__ == "__main__":
    app.run(debug=True)