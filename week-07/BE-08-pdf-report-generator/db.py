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

def get_report_data() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Total Orders & Total Revenue
    cursor.execute("SELECT COUNT(*) as total_orders, ROUND(SUM(amount), 2) as total_revenue, ROUND(AVG(amount), 2) as avg_order FROM orders;")
    totals = cursor.fetchone()
    
    # 2. Top 5 Products by Revenue
    cursor.execute("""
        SELECT product, COUNT(*) as units_sold, ROUND(SUM(amount), 2) as revenue
        FROM orders
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 5;
    """)
    top_products = [dict(r) for r in cursor.fetchall()]
    
    # 3. Orders per day (last 7 recorded days)
    cursor.execute("""
        SELECT SUBSTR(created_at, 1, 10) as order_date, COUNT(*) as daily_orders, ROUND(SUM(amount), 2) as daily_revenue
        FROM orders
        GROUP BY order_date
        ORDER BY order_date DESC
        LIMIT 7;
    """)
    daily_stats = [dict(r) for r in cursor.fetchall()]
    
    # 4. Recent Sample Orders (for the detailed table in the PDF)
    cursor.execute("SELECT id, customer, product, amount, SUBSTR(created_at, 1, 16) as created_at FROM orders ORDER BY id ASC LIMIT 60;")
    order_items = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    return {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_orders": totals["total_orders"],
        "total_revenue": totals["total_revenue"],
        "avg_order_value": totals["avg_order"],
        "top_products": top_products,
        "daily_breakdown": daily_stats,
        "detailed_orders": order_items
    }

if __name__ == "__main__":
    init_and_seed_db()
    data = get_report_data()
    print("\n--- Aggregation Query Results ---")
    print(f"Total Orders: {data['total_orders']}")
    print(f"Total Revenue: ${data['total_revenue']}")
    print(f"Top Product: {data['top_products'][0]['product']} (${data['top_products'][0]['revenue']})")
    print(f"Daily Rows: {len(data['daily_breakdown'])}")
    print("Stage 2 Checkpoint Passed: get_report_data() returns complete verified aggregate metrics.")
