import sqlite3
import getpass
import os
import time
from InquirerPy import prompt

from db import DB_PATH
from bcolors import bcolors
from models import fetch_user_password

def welcome_page() -> None: 
    while True:
        os.system("cls")
        print(bcolors.HEADER + "Welcome to Motor Mile!" + bcolors.ENDC)
        print(bcolors.OKGREEN + "Login to get started!" + bcolors.ENDC)

        username: str = input("Username: ")
        fetched_password = fetch_user_password(username)

        questions = [{
            "type": "password",
            "name": "password",
            "message": "Password:",
            "transformer": lambda _: "[hidden]",
        }]

        result = prompt(questions)
        if result["password"] == fetched_password:
            os.system("cls")
            print(bcolors.OKGREEN + "Welcome, " + username + "!" + bcolors.ENDC)
            # wait for any user input to continue
            input("\nPress enter to continue...")
            return
        else:
            print(bcolors.FAIL + "Incorrect password or username. Try again." + bcolors.ENDC)
            questions = [
                {
                    "type": "confirm",
                    "message": "Would you like to try again?",
                    "name": "try_again",
                }
            ]

            result = prompt(questions)
            if not result["try_again"]:
                return

            continue