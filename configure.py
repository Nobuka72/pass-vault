import os
import sys
import string
import random
import hashlib
import sys
from getpass import getpass
from utils.dbconfig import dbconfig

def config_check():
    conn = dbconfig()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM pm.secrets"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    if results[0][0] !=0:
        return True
    else:
        return False
    

def devicesecret(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret = ''.join(random.choice(characters) for _ in range(length))
    return secret

def makeconfig():
    if checkconfig():
        print("Configuration already exists.")
        return  
    
    print("Creating configuration.")

    db=dbconfig()
    cursor = db.cursor()   
    try:
        cursor.execute("CREATE SCHEMA pm;")
    except Exception as e:
        print(f"Error creating schema: {e}")
        console.print_exception(show_locals=True)
        db.close()
        sys.exit(0)

    print("schema 'pm' created successfully.")

    query="create table pm.secrets (id serial primary key, masterkey_hash varchar(64) not null, devicesecret varchar(64) not null);"
    cursor.execute(query)
    print("table 'secrets' created successfully.")
    query = "CREATE TABLE pm.entries (site_name TEXT NOT NULL, site_url TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    cursor.execute(query)
    print("Table 'entries' created successfully.")

    mp= ""
    print("[bold]MASTER PASSWORD[/bold] is only password you will need to remember in order to access the password vault:")

    while True:
        mp = getpass("Enter Master Password: ")
        mpc = getpass("Confirm Master Password: ")
        if mp != mpc:
            print("[red][!] Master Passwords do not match! Please try again. [/red]")
        else:
            break 

    #hashing the master password
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    print("[green][+][/green] generated hash of master password.")


    query= "INSERT INTO pm.secrets (masterkey_hash, devicesecret) VALUES (%s, %s)"
    val = (hashed_mp, devicesecret())
    cursor.execute(query, val)
    db.commit()
    print("[green][+][/green] Master Password and Device Secret stored successfully.")
    db.close()

def delete():
        print("deleting a configuaration cleares all stored passwords & this process irreversible!")
        while True:
            confirm = input("Are you sure you want to delete the configuration? (yes/no): ")
            if confirm.lower() == 'yes':
                conn = dbconfig()
                cursor = conn.cursor()
                cursor.execute("DROP SCHEMA pm CASCADE;")
                conn.commit()
                conn.close()
                print("[green][+][/green] Configuration deleted successfully.")
                break
            elif confirm.lower() == 'no'or confirm.lower() == "":
                sys.exit(0)
                print("[green][+][/green] Deletion cancelled.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                return

def checkconfig():
    conn = dbconfig()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM pm.secrets"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    if results[0][0] !=0:
        return True
    else:
        return False
    
def remake():
    print("remaking configuration will delete all stored passwords!")
    delete()
    makeconfig()
    return 

if __name__ == "__main__":

    if(len(sys.argv)!=2):
        print("Usage: python configure.py [make|remake|delete|check]")
        sys.exit(0) 
    if sys.argv[1]=="remake":
        remake()
    elif sys.argv[1]=="delete":
        delete()
    elif sys.argv[1]=="check":
        if checkconfig():
            print("Configuration exists.")
        else:
            print("No configuration found.")
    else:
        print("usage: python configure.py [make|remake|delete|check]")
        sys.exit(0) 