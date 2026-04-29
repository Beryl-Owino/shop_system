# ==============================
# TEST FILE
# ==============================

from mpesa_loader import process_mpesa_data

df = process_mpesa_data("mpesa_simulated.csv")

print(df.head())