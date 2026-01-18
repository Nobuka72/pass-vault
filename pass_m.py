import argparse
from getpass import getpass
import hashlib
import pyperclip

import utils.retrieve
import utils.add
import utils.generate
from utils.dbconfig import dbconfig
from utils.aesutil import encryptor, decryptor

parser = argparse.ArgumentParser(description="Description")

parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument("-s", "--name", help="site name")
parser.add_argument("-u", "--url", help="site url")
parser.add_argument("-n", "--login", help="username")
parser.add_argument("-e", "--email", help="email")
parser.add_argument("-l", "--length", type=int, help="length of password to generate")
parser.add_argument("-c", "--copy", action='store_true', help="copy generated password to clipboard")


args=parser.parse_args()

def inputandvalidationmasterpass():
    mp=getpass("Enter Master Password: ")
    mpc=getpass("Confirm Master Password: ")
    hashed_mp=hashlib.sha256(mp.encode()).hexdigest()
    conn = dbconfig()
    cursor = conn.cursor()
    query = "SELECT masterkey_hash, devicesecret FROM pm.secrets"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    if hashed_mp !=results[0][0]:
        print("[!] Incorrect Master Password!")
        exit()
    if mp!=mpc:
        print("Master Passwords do not match!")
        exit()
    return [mp, results[0][1]]

def main():
    if args.option in ['a', 'add']:
        if args.name is None or args.url is None or args.login is None:
            if args.name is None:
                print("[!] Site name is required to add an entry!")
            if args.url is None:
                print("[!] Site URL is required to add an entry!")
            if args.login is None:
                print("[!] Username is required to add an entry!")
            exit()

        if args.email is None:
            args.email = ""
        password = getpass("Enter Password to store: ")
        mp_ds = inputandvalidationmasterpass()
        if mp_ds is not None:
            utils.add.add_entry(mp_ds[0], mp_ds[1], args.name, args.url, args.login, args.email, password)

    elif args.option in ['e', 'extract']:
        mp_ds = inputandvalidationmasterpass()
        search = {}
        if args.name is not None:
            search['site_name'] = args.name
        if args.url is not None:
            search['site_url'] = args.url
        if args.login is not None:
            search['username'] = args.login
        if args.email is not None:
            search['email'] = args.email
        if mp_ds is not None:
            result=utils.retrieve.retrieve_password(mp_ds[0], mp_ds[1], search, decrypt=True)
            if args.copy and result is not None:
                pyperclip.copy(result)
                print("[+] Password copied to clipboard!") 

    elif args.option in ['g', 'generate']:
        if args.length is None:
            print("[!] Length of password to generate is required!")
            exit()
        password=utils.generate.create_password(args.length, True, True)
        print(f"[+] Generated Password: {password}")
        if args.copy:
            pyperclip.copy(password)
            print("[+] Password copied to clipboard!")               

if __name__ == "__main__":
    main()

# import tkinter as tk
# from tkinter import messagebox, simpledialog
# from utils.database_manager import DatabaseManager
# from utils.password_generator import create_password

# tk.geometry("600x500")
# tk.title("Password Manager - Password Generator")
# tk.resizable(False, False)
# tk.configure(bg="#f0f0f0")
# tk.mainloop()
