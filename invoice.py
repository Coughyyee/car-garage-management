from db import DB_PATH
from bcolors import bcolors
import models

from InquirerPy import prompt
from InquirerPy.validator import NumberValidator
import sqlite3
import os

def generate_invoice() -> None:
    # input customer details
    # input vehicle information
    # input date of service
    # input list of parts
    # input labor costs --
    # input sales tax --
    questions = [
        {
            "type": "input",
            "message": "Enter customer name:",
            "name": "customer_name",
        },
        {
            "type": "input",
            "message": "Enter customer last name:",
            "name": "customer_last_name",
        },
        {
            "type": "input",
            "message": "Enter vehicle make:",
            "name": "vehicle_make",
        },
        {
            "type": "input",
            "message": "Enter vehicle model:",
            "name": "vehicle_model",
        },
        {
            "type": "input",
            "message": "Enter date of service (YYYY-MM-DD):",
            "name": "date",
        },
        {
            "type": "input",
            "message": "Enter time taken (HH:MM):",
            "name": "time_taken",
        },
        {
            "type": "input",
            "message": "Enter list of parts (a, b, c...):",
            "name": "parts",
        },
    ]

    result = prompt(questions)

    time_taken = result["time_taken"]

    time_taken_list = time_taken.split(":")
    hours = int(time_taken_list[0])
    minutes = int(time_taken_list[1])
    total_time: float = hours + (minutes / 60)

    total_cost: float = 0.0

    # split the list of parts into individual parts
    parts_list = result["parts"].split(", ")

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
    
    labor_costs = models.fetch_labor_costs()
    sales_tax = models.fetch_sales_tax()

    total_cost += labor_costs * total_time
    total_cost *= (1 + sales_tax)

    # confirmation
    confirmation = prompt([
        {
            "type": "confirm",
            "message": "Are you sure you want to generate the invoice?",
            "default": False,
            "name": "confirm",
        },
    ])

    confirmation = confirmation["confirm"]

    if not confirmation:
        os.system("cls")
        print(bcolors.FAIL + "Invoice generation cancelled." + bcolors.ENDC)
        input(bcolors.WARNING + "Press enter to continue..." + bcolors.ENDC)
        return

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
    
    # remove parts from inventory
    for part in parts_list:
        # TODO: check if part is going to be negative value - do not allow operation.
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("UPDATE inventory SET quantity = quantity - 1 WHERE name = ?", (part,))
        con.commit()
        con.close()

    # format invoice
    invoice = f"""Invoice for {result["customer_name"].capitalize()} {result["customer_last_name"].capitalize()} 
Date: {result["date"]}
Parts: {parts_list}
Time Taken: {hours} hours {minutes} minutes
Labor Costs: £{round(labor_costs, 2):.2f}
Sales Tax: {(sales_tax* 100)}%
Total Cost: £{round(total_cost, 2):.2f}
"""

    # output invoice
    print(bcolors.OKBLUE + invoice + bcolors.ENDC)

    # save document to .txt file
    invoice_dir = f"invoices/{result['customer_name'].capitalize()}-{result['customer_last_name'].capitalize()}"
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)
    with open(os.path.join(invoice_dir, f"{result['customer_last_name'].capitalize()}_{result['date']}_invoice.txt"), "w") as f:
        f.write(invoice)

    print(bcolors.OKGREEN + "Invoice saved to invoice.txt." + bcolors.ENDC)

    # wait for any user input to continue
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)

    return

def generate_invoice_with_details(parts_list: list, total_cost: float, labor_costs: float, sales_tax: float, time_taken_list: list) -> None:
    # input customer details
    # input vehicle information
    # input date of service
    # input list of parts
    # input labor costs --
    # input sales tax --
    questions = [
        {
            "type": "input",
            "message": "Enter customer name:",
            "name": "customer_name",
        },
        {
            "type": "input",
            "message": "Enter customer last name:",
            "name": "customer_last_name",
        },
        {
            "type": "input",
            "message": "Enter vehicle make:",
            "name": "vehicle_make",
        },
        {
            "type": "input",
            "message": "Enter vehicle model:",
            "name": "vehicle_model",
        },
        {
            "type": "input",
            "message": "Enter date of service (YYYY-MM-DD):",
            "name": "date",
        },
    ]

    result = prompt(questions)

    # confirmation
    confirmation = prompt([
        {
            "type": "confirm",
            "message": "Are you sure you want to generate the invoice?",
            "default": False,
            "name": "confirm",
        },
    ])

    confirmation = confirmation["confirm"]

    if not confirmation:
        os.system("cls")
        print(bcolors.FAIL + "Invoice generation cancelled." + bcolors.ENDC)
        input(bcolors.WARNING + "Press enter to continue..." + bcolors.ENDC)
        return

    # remove parts from inventory
    for part in parts_list:
        # TODO: check if part is going to be negative value - do not allow operation.
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("UPDATE inventory SET quantity = quantity - 1 WHERE name = ?", (part,))
        con.commit()
        con.close()

    # format invoice
    invoice = f"""Invoice for {result["customer_name"].capitalize()} {result["customer_last_name"].capitalize()} 
Date: {result["date"]}
Parts: {parts_list}
Time Taken: {time_taken_list[0]} hours {time_taken_list[1]} minutes
Labor Costs: £{round(labor_costs, 2):.2f}
Sales Tax: {(sales_tax * 100)}%
Total Cost: £{round(total_cost, 2):.2f}
"""

    # output invoice
    print(bcolors.OKBLUE + invoice + bcolors.ENDC)

    # save document to .txt file
    invoice_dir = f"invoices/{result['customer_name'].capitalize()}-{result['customer_last_name'].capitalize()}"
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)
    with open(os.path.join(invoice_dir, f"{result['customer_last_name'].capitalize()}_{result['date']}_invoice.txt"), "w") as f:
        f.write(invoice)

    print(bcolors.OKGREEN + "Invoice saved to invoice.txt." + bcolors.ENDC)

    # wait for any user input to continue
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)

    return