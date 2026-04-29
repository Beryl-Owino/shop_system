import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# SETTINGS
# -----------------------------
transaction_types = [
    "Customer Payment",
    "Paybill",
    "Buy Goods",
    "Withdrawal"
]

base_date = datetime(2026, 4, 1)

data = []

# -----------------------------
# GENERATE SAMPLE DATA
# -----------------------------
for i in range(200):  # 200 transactions
    date = base_date + timedelta(minutes=random.randint(0, 60*24*30))

    t_type = random.choices(
        transaction_types,
        weights=[50, 20, 15, 15],
        k=1
    )[0]

    if t_type == "Withdrawal":
        amount = -random.randint(500, 5000)
    else:
        amount = random.randint(50, 3000)

    balance = random.randint(1000, 20000)

    receipt = f"MP{random.randint(100000,999999)}"

    data.append([
        receipt,
        date.strftime("%Y-%m-%d %H:%M:%S"),
        t_type,
        amount,
        balance
    ])

# -----------------------------
# CREATE DATAFRAME
# -----------------------------
df = pd.DataFrame(data, columns=[
    "receipt", "date", "type", "amount", "balance"
])

# Save file
df.to_csv("mpesa_simulated.csv", index=False)

print("Dataset created successfully!")