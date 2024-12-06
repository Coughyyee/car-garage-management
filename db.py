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
    set_default_parts_prices()
    set_default_tools_prices()

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


def set_default_parts_prices() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for item in [('brakes', 100), ('battery', 130), ('alternator', 250), ('engine', 1000), ('radiator', 400), ('muffler', 135), ('axels', 1250), ('spark plugs', 85), ('clutch', 1400), ('cooling system', 300), ('tire', 70), ('windshield wipers', 25), ('shock absorbers', 250)]:
        cur.execute("SELECT id FROM inventory WHERE name = ?", (item[0],))
        item_exists = cur.fetchone()

        if item_exists:
            # Update existing item
            cur.execute("UPDATE inventory SET price = ? WHERE name = ?", (item[1], item[0]))
        else:
            # Insert new item
            cur.execute("INSERT INTO inventory (name, price, quantity, expiration_date) VALUES (?, ?, 10, '2023-01-01')", (item[0], item[1]))

    con.commit()
    con.close()
  
def set_default_tools_prices() -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for item in [('Screwdrivers', 15), ('Socket sets', 15), ('Impact wrench', 15), ('Wrenches', 15), ('Torque wrench', 15), ('Diagnostic tools', 15), ('Pliers', 15), ('Drill', 15), ('Gloves', 15), ('Tire gauge', 15), ('Engine tools', 15), ('Wire stripper', 15), ('Jack stands', 15), ('Pry bars', 15), ('Funnels', 15), ('Oil filter remover tool', 15), ('Oil drain tray (or bucket)', 15), ('Telescoping mirror', 15)]:
        cur.execute("SELECT id FROM inventory WHERE name = ?", (item[0],))
        item_exists = cur.fetchone()

        if item_exists:
            # Update existing item
            cur.execute("UPDATE inventory SET price = ? WHERE name = ?", (item[1], item[0]))
        else:
            # Insert new item
            cur.execute("INSERT INTO inventory (name, price, quantity, expiration_date) VALUES (?, ?, 5, '2023-01-01')", (item[0], item[1]))

    con.commit()
    con.close()

# DEV ONLY