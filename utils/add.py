from utils.dbconfig import dbconfig
from utils.aesutil import *
from getpass import getpass
import base64
import secrets


from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256


def master_key(mp,ds):
    password=mp.encode()
    salt=ds.encode()
    key=PBKDF2(password,salt,dkLen=32,count=100000, hmac_hash_module=SHA256)
    return key

def check_entry(site_name, site_url, username, email):
    conn = dbconfig()
    cursor = conn.cursor()

    query = "SELECT * FROM pm.entries WHERE site_name=%s AND site_url=%s AND username=%s AND email=%s"
    cursor.execute(query, (site_name, site_url, username, email))
    results = cursor.fetchall()

    if len(results)!=0:
        return True
    else:
        return False
    


def add_entry(mp, ds, site_name, site_url, username, email, password):
    if check_entry(site_name, site_url, username, email):
        print("Entry already exists.")
        return

    mk=master_key(mp, ds)
    encrypted_password = encryptor(key=mk, source=password.encode(), keytype="bytes")

    conn = dbconfig()
    cursor = conn.cursor()

    query = "INSERT INTO pm.entries (site_name, site_url, username, email, password) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (site_name, site_url, username, email, encrypted_password))
    conn.commit()
    print("Entry added successfully.")
    conn.close()