import sqlite3
import os

DB_PATH = "db/motor_mile.db"

def initialize_db() -> None:
    # check if the database file exists in db directory.
    try:
        if not os.path.exists(DB_PATH):
            # create the file 'motor_miles.db'
            con = sqlite3.connect(DB_PATH)
            con.close()
        # create the database tables if they dont exist
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price INTEGER, expiration_date TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS costs (id INTEGER PRIMARY KEY, labor_cost FLOAT, sales_tax_percent FLOAT)")
        con.commit()
        con.close()
    except Exception as e:
        print(e)
        os.exit(1)

# DEV ONLY
def add_default_data() -> None:
    add_default_user()
    add_default_costs()

    set_default_wrench_quantity()

def add_default_user() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Check if admin user exists
    cur.execute("SELECT id FROM users WHERE username = 'admin'")
    admin_exists = cur.fetchone()
    
    if admin_exists:
        # Update existing admin user
        cur.execute("UPDATE users SET password = 'password' WHERE username = 'admin'")
    else:
        # Create new admin user
        cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'password')")
    
    con.commit()
    con.close()

def add_default_costs() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Check if default costs exist
    cur.execute("SELECT id FROM costs LIMIT 1")
    costs_exist = cur.fetchone()
    
    if costs_exist:
        # Update existing costs
        cur.execute("UPDATE costs SET labor_cost = 50.00, sales_tax_percent = 0.20 WHERE id = ?", (costs_exist[0],))
    else:
        # Insert new costs
        cur.execute("INSERT INTO costs (labor_cost, sales_tax_percent) VALUES (50.00, 0.20)")
    
    con.commit()
    con.close()

def set_default_wrench_quantity() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("UPDATE inventory SET quantity = 10 WHERE name = 'wrench'")
    con.commit()
    con.close()

# DEV ONLY
