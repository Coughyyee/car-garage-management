import sqlite3
import getpass
import os
import time

from db import DB_PATH
from bcolors import bcolors

def welcome_page() -> None: 
    while True:
        os.system("cls")
        print(bcolors.HEADER + "Welcome to Motor Mile!" + bcolors.ENDC)
        print(bcolors.OKGREEN + "Login to get started!" + bcolors.ENDC)
        username: str = input("Username: ")
        password: str = getpass.getpass("Password: ")
        logged_in = login_system(username, password)
        if logged_in:
            os.system("cls")
            print(bcolors.OKGREEN + "Welcome, " + username + "!" + bcolors.ENDC)
            # wait for any user input to continue
            input("\nPress enter to continue...")
            return

def login_system(username: str, password: str) -> bool:
    # call DB to check if username exists
    # if it does, check if password is correct
    # if it is let the user in.
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        if user is not None:
            print(bcolors.OKGREEN + "Login successful!" + bcolors.ENDC)
            return True
        else:
            print(bcolors.FAIL + "Incorrect username or password." + bcolors.ENDC)
            print(bcolors.FAIL + "Please try again...." + bcolors.ENDC)
            time.sleep(1)
            return False
    except Exception as e:
        print(e)
        os.exit(1)

