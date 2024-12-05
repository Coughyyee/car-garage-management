import getpass
import sqlite3
import os
import time
from InquirerPy import prompt

from manage_inventory import manage_inventory
from bcolors import bcolors
from db import DB_PATH, initialize_db
from login import welcome_page
from invoice import generate_invoice
from service_costs import calculate_service_costs
from db import add_default_data

def prompt_main() -> None:
    while True:
        os.system("cls")
        questions = [
            {
                "type": "list",
                "message": "What would you like to do?",
                "choices": ["Manage Inventory", "Generate Invoice", "Calculate Service Costs", "Manage Account", "Logout", "Exit"],
                "name": "what_would_you_like_to_do",
            },
        ]
        result = prompt(questions, style={"questionmark": "fg:#e5c07b bold", "pointer": "#61afef"})
        choice = result["what_would_you_like_to_do"]
        if choice == "Manage Inventory":
            manage_inventory()
        elif choice == "Generate Invoice":
            generate_invoice()
        elif choice == "Calculate Service Costs":
            calculate_service_costs()
        elif choice == "Manage Account":
            pass
        elif choice == "Logout":
            welcome_page()
        elif choice == "Exit":
            os.system("cls")
            exit(0)
        

        # os.system("cls")
        # print(bcolors.HEADER + "Welcome!" + bcolors.ENDC)
        # print(bcolors.HEADER + "What would you like to do?" + bcolors.ENDC)
        # print("1. Manage Inventory")
        # print("2. Generate Invoice")
        # print("3. Calculate Service Costs")
        # print("4. Manage Account")
        # print("5. Logout")
        # print(bcolors.FAIL + "6. Exit" + bcolors.ENDC)

        # try:
        #     choice: int = int(input("> "))
        # except ValueError:
        #     print("Invalid Input try again!")
        #     continue

        # if choice == 1:
        #     manage_inventory()
        # elif choice == 2:
        #     pass
        # elif choice == 3:
        #     pass
        # elif choice == 4:
        #     pass
        # elif choice == 5:
        #     welcome_page()
        # elif choice == 6:
        #     os.system("cls")
        #     exit(0)

def main() -> None:
    initialize_db()
    add_default_data() # DEV ONLY
    welcome_page()
    prompt_main()


if __name__ == '__main__':
    main()