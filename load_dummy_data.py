from shop_db import add_sale

# ==============================
# DUMMY SALES DATA
# ==============================
dummy_sales = [
    ("chips", "regular", 10, 120, 70, "2026-04-10 10:30:00"),
    ("chips", "masala", 5, 130, 80, "2026-04-10 12:00:00"),
    ("soda", "300ml", 20, 40, 28, "2026-04-10 13:15:00"),

    ("chips", "regular", 8, 120, 70, "2026-04-09 11:00:00"),
    ("soda", "500ml", 15, 60, 45, "2026-04-09 14:30:00"),
    ("smokie", "single", 25, 30, 15, "2026-04-09 18:00:00"),

    ("chips", "masala", 12, 130, 80, "2026-04-08 09:45:00"),
    ("soda", "300ml", 30, 40, 28, "2026-04-08 12:20:00"),
    ("smokie", "single", 18, 30, 15, "2026-04-08 17:10:00"),
]

# ==============================
# INSERT DATA
# ==============================
for sale in dummy_sales:
    item, variant, qty, price, cost, date = sale

    # we reuse your add_sale logic but override date manually
    from shop_db import cursor, conn

    cursor.execute("""
        INSERT INTO sales (item, variant, qty, price, cost, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (item, variant, qty, price, cost, date))

conn.commit()

print("Dummy data inserted successfully!")