from mpesa_loader import process_mpesa_data
from shop_db import create_mpesa_table, add_mpesa_transaction, close_connection

# Step 1: Load and process CSV
df = process_mpesa_data("mpesa_simulated.csv")

# Step 2: Ensure table exists
create_mpesa_table()

# Step 3: Insert data into DB
for _, row in df.iterrows():
    add_mpesa_transaction(
        row["receipt"],
        str(row["date"]),
        row["type"],
        row["amount"],
        row["balance"],
        row["category"]
    )

print("M-Pesa data inserted successfully!")

# Step 4: Close DB
close_connection()