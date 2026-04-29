import sqlite3
from datetime import datetime

DB_NAME = "shop.db"

# =========================
# CREATE TABLES
# =========================
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            variant TEXT,
            qty INTEGER,
            price INTEGER,
            cost INTEGER,
            date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mpesa_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt TEXT,
            date TEXT,
            type TEXT,
            amount REAL,
            balance REAL,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# INSERT SALES
# =========================
def add_sale(item, variant, qty, price, cost):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO sales (item, variant, qty, price, cost, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (item, variant, qty, price, cost, date))

    conn.commit()
    conn.close()


# =========================
# INSERT MPESA
# =========================
def add_mpesa_transaction(receipt, date, t_type, amount, balance, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mpesa_transactions 
        (receipt, date, type, amount, balance, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (receipt, date, t_type, amount, balance, category))

    conn.commit()
    conn.close()


# =========================
# FETCH SALES
# =========================
def get_sales():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, item, variant, qty, price, cost, date FROM sales
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

# =========================
# DELETE & UPDATE SALES
# =========================

def delete_sale(sale_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
    conn.commit()
    conn.close()

def update_sale(sale_id, item, variant, qty, price, cost):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sales
        SET item=?, variant=?, qty=?, price=?, cost=?
        WHERE id=?
    """, (item, variant, qty, price, cost, sale_id))
    conn.commit()
    conn.close()

# =========================
# FETCH MPESA
# =========================
def get_mpesa_transactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT receipt, date, type, amount, balance, category 
        FROM mpesa_transactions
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows