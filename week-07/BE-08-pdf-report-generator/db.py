import sqlite3
import os
import random
import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "report.db")

CUSTOMERS = ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", "Evan Wright", "Fiona Gallagher", "George Clark"]
PRODUCTS = [
    ("Pro Subscription", 49.00),
    ("Enterprise License", 299.00),
    ("API Usage Pack (100k)", 25.00),
    ("Dedicated Support Tier", 150.00),
    ("Custom Model Training", 500.00)
]

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_and_seed_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    """)
    
    # 2. Reports metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            date_key TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Idempotent seed: delete existing orders to prevent duplicate row counts
    cursor.execute("DELETE FROM orders;")
    
    # Seed exactly 200 orders distributed over the last 14 days
    now = datetime.datetime.now()
    orders_to_insert = []
    
    random.seed(42) # Deterministic seed for reproducible numbers
    for _ in range(200):
        customer = random.choice(CUSTOMERS)
        product_name, base_price = random.choice(PRODUCTS)
        # Random variance in amount
        amount = round(base_price * random.uniform(0.9, 1.1), 2)
        days_ago = random.randint(0, 14)
        order_time = (now - datetime.timedelta(days=days_ago, hours=random.randint(0, 23))).isoformat()
        orders_to_insert.append((customer, product_name, amount, order_time))
        
    cursor.executemany("INSERT INTO orders (customer, product, amount, created_at) VALUES (?, ?, ?, ?)", orders_to_insert)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    conn.close()
    print(f"Seeded report.db with exactly {count} orders.")
    return count

if __name__ == "__main__":
    init_and_seed_db()
    # Run second time to verify idempotency
    count2 = init_and_seed_db()
    assert count2 == 200
    print("Stage 1 Checkpoint Passed: Idempotent seed verified (200 orders).")
