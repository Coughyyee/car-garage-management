import sqlite3
from InquirerPy import prompt
from invoice import generate_invoice_with_details
from db import DB_PATH
from bcolors import bcolors
import models

def calculate_service_costs() -> None:
    # input parts used
    # input time taken
    questions = [
        {
            "type": "input",
            "message": "Enter parts used (a, b, c...):",
            "name": "parts_used",
        },
        {
            "type": "input",
            "message": "Enter time taken (HH:MM):",
            "name": "time_taken",
        }
    ]

    result = prompt(questions)
    parts_used = result["parts_used"]
    time_taken = result["time_taken"]

    time_taken_list = time_taken.split(":")
    hours = int(time_taken_list[0])
    minutes = int(time_taken_list[1])
    total_time: float = hours + (minutes / 60)

    total_cost: float = 0.0

    parts_list = parts_used.split(", ")

    # find the price of each part in the inventory table in the database
    for part in parts_list:
        # query the database for the price of the part
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT price FROM inventory WHERE name = ?", (part,))
        price = cur.fetchone()[0] 
        con.close()
        if price is None:
            print(f"Part {part} not found in inventory.")
            continue # continue to the next part
        # add the price of the part to the total cost
        total_cost += price
    
    
    # check if any part in inventory is out of stock
    for part in parts_list:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT quantity FROM inventory WHERE name = ?", (part,))
        quantity = cur.fetchone()[0] 
        con.close()
        if quantity == 0:
            print(bcolors.FAIL + f"Part {part} is out of stock!" + bcolors.ENDC)
            input(bcolors.WARNING + "Press enter to continue..." + bcolors.ENDC)
            return
    

    # get labor costs data from db
    labor_cost = models.fetch_labor_costs()

    # retrieve tax rates from db
    tax_rates_percent = models.fetch_sales_tax()

    # calculate total labor costs
    labor_cost *= total_time
    total_cost += labor_cost
    total_cost *= (1 + tax_rates_percent)

    # round total cost to 2 decimal places
    total_cost = round(total_cost, 2)

    # print total costs
    print(bcolors.OKGREEN + f"Total cost: £{total_cost:.2f}" + bcolors.ENDC)

    # create invoice prompt
    confirmation = prompt([
        {
            "type": "confirm",
            "message": "Do you want to create an invoice with these details?",
            "default": False,
            "name": "confirm",
        },
    ])

    confirmation = confirmation["confirm"]

    # if confirmation, go generate invoice
    if confirmation:
        # TODO?: idk if recieveing from sql returns in string or the actual data type
        generate_invoice_with_details(parts_list, total_cost, labor_cost, tax_rates_percent, time_taken_list)
        return 
    
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)
    return