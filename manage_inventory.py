import os
import sqlite3
from InquirerPy import prompt

from db import DB_PATH
from bcolors import bcolors

def manage_inventory() -> None:
    while True:
        # check if anything in the inventory is low stock (less than 5) and if it is near expiration date.
        # if it is, notify the user.
        os.system("cls")
        print(bcolors.HEADER + "Inventory Management" + bcolors.ENDC)
        print("Checking Inventory...")
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT * FROM inventory WHERE quantity < 5")
        low_stock = cur.fetchall()
        # cur.execute("SELECT * FROM inventory WHERE expiration_date < ? AND quantity > 0", (time.strftime("%Y-%m-%d",)))
        # near_expiration = cur.fetchall()
        con.close()
        os.system("cls")

        print(bcolors.HEADER + "Inventory Management" + bcolors.ENDC)
        if len(low_stock) > 0:
            print(bcolors.WARNING + "Low Stock Items:" + bcolors.ENDC)
            for item in low_stock:
                print(f"\t{item[1]}: {item[2]}")
        # if len(near_expiration) > 0:
        #     print("Near Expiration Items:")
        #     for item in near_expiration:
        #         print(f"{item[1]}: {item[2]}")

        print()
        questions = [
            {
                "type": "list",
                "message": "What would you like to do?",
                "choices": ["List all parts", "List specific part", "Add specific part", "Remove specific part", "Go back"],
                "name": "what_would_you_like_to_do",
            }
        ]

        answer = prompt(questions, style={"questionmark": "fg:#e5c07b bold", "pointer": "#61afef"})
        if answer["what_would_you_like_to_do"] == "List all parts":
            list_inventory()
        elif answer["what_would_you_like_to_do"] == "List specific part":
            list_specific_part()
        elif answer["what_would_you_like_to_do"] == "Add specific part":
            add_specific_part()
        elif answer["what_would_you_like_to_do"] == "Remove specific part":
            remove_specific_part()
        elif answer["what_would_you_like_to_do"] == "Go back":
            return


        # print()
        # print(bcolors.HEADER + "What would you like to do?" + bcolors.ENDC)
        # print("1. List all parts")
        # print("2. List specific part")
        # print("3. Add specific part")
        # print("4. Remove specific part")
        # print(bcolors.FAIL + "5. Go back" + bcolors.ENDC)

        # try:
        #     choice: int = int(input("> "))
        # except ValueError:
        #     print(bcolors.FAIL + "Invalid Input try again!" + bcolors.ENDC)
        #     continue

        # if choice == 1:
        #     list_inventory()
        # elif choice == 2:
        #     list_specific_part()
        # elif choice == 3:
        #     add_specific_part()
        # elif choice == 4:
        #     remove_specific_part()
        # elif choice == 5:
        #     return

def list_inventory() -> None:
    os.system("cls")
    print(bcolors.HEADER + "List Inventory" + bcolors.ENDC)
    print("Listing all parts...")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM inventory")
    results = cur.fetchall()
    con.close()
    os.system("cls")
    print(bcolors.HEADER + "List Inventory" + bcolors.ENDC)
    for result in results:
        print(f"\t{result[1]}: quantity: {result[2]}, price: {result[3]}, expiration date: {result[4]}")

    # wait for any user input to continue
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)

def list_specific_part() -> None:
    os.system("cls")
    print(bcolors.HEADER + "List Specific Part" + bcolors.ENDC)
    part_name: str = input("Enter part name: ")
    print("Listing specific part...")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM inventory WHERE name = ?", (part_name,))
    results = cur.fetchall()
    con.close()
    os.system("cls")
    print(bcolors.HEADER + "List Specific Part" + bcolors.ENDC)
    if len(results) == 0:
        print(bcolors.FAIL + "No results found!" + bcolors.ENDC)
    else:
        for result in results:
            print(f"\t{result[1]}: quantity: {result[2]}, price: {result[3]}, expiration date: {result[4]}")

    # wait for any user input to continue
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)

def add_specific_part() -> None:
    os.system("cls")
    print(bcolors.HEADER + "Add Specific Part" + bcolors.ENDC)
    part_name: str = input("Enter part name: ")
    part_quantity: int = int(input("Enter part quantity: "))
    part_price: int = int(input("Enter part price (£): "))
    part_expiration_date: str = input("Enter part expiration date: ")
    print("Adding specific part...")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO inventory (name, quantity, price, expiration_date) VALUES (?, ?, ?, ?)", (part_name, part_quantity, part_price, part_expiration_date))
    con.commit()
    con.close()
    os.system("cls")
    print(bcolors.HEADER + "Add Specific Part" + bcolors.ENDC)
    print("Part added successfully!")

    # wait for any user input to continue
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)

def remove_specific_part() -> None:
    os.system("cls")
    print(bcolors.HEADER + "Remove Specific Part" + bcolors.ENDC)
    part_name: str = input("Enter part name: ")
    print("Removing specific part...")
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM inventory WHERE name = ?", (part_name,))
    con.commit()
    con.close()
    os.system("cls")
    print(bcolors.HEADER + "Remove Specific Part" + bcolors.ENDC)
    if cur.rowcount == 0:
        print(bcolors.FAIL + "No results found!" + bcolors.ENDC)
    else:
        print("Part removed successfully!")

    # wait for any user input to continue
    input(bcolors.WARNING + "\nPress enter to continue..." + bcolors.ENDC)
