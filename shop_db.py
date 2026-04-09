import sqlite3

# Connect to the database(creates file if it doesn't exist)
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Function to add sales
def add_sale(item, variant, qty, price, cost):
    cursor.execute("""
    INSERT INTO sales(item, variant, qty, price, cost)
    VALUES(?, ?, ?, ?, ?)
    """,(item, variant, qty, price, cost))

# save chamges
    conn.commit()
    print(f"Added:{item}-{variant}")

# Getting user input
print("\nEnter new sale details:")
item = input("Item name: ")
variant = input("Variant: ")
qty = input("Quantity: ")
price = input("Price: ")
cost = input("Cost: ")


# Inserting into the database
add_sale(item, variant,)
