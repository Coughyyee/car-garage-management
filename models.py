import sqlite3
from db import DB_PATH

def fetch_labor_costs() -> float:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT labor_cost FROM costs")
    labor_cost = cur.fetchone()
    con.close()
    return labor_cost[0]

def fetch_sales_tax() -> float:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT sales_tax_percent FROM costs")
    sales_tax = cur.fetchone()
    con.close()
    return sales_tax[0]