from .dbconfig import dbconfig
import pyperclip
import utils.aesutil
import secrets
import base64

from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256



def master_key(mp,ds):
    password=mp.encode()
    salt=ds.encode()
    key=PBKDF2(password,salt,dkLen=32,count=100000, hmac_hash_module=SHA256)
    return key

def retrieve_password(mp, ds, search, decrypt=True):
    conn = dbconfig()
    cursor = conn.cursor()

    query = ""
    if len(search) == 0:
        query= "SELECT * FROM pm.entries"
    else:
        query= "SELECT * FROM pm.entries limit 100 "
        for i in search:
            query+=f"{i} = '{search[i]}' AND "
        query=query[:-5] + " LIMIT 1"
        cursor.execute(query)
        results=cursor.fetchall()
        

        if len(results) == 0:
            print("No matching entries found.")
            return
        
        if len(results) > 1:
            print("Multiple entries found. Please refine your search criteria.")

            table = (table =="Results")
            table.add_column("site name", style="cyan", no_wrap=True)
            table.add_column("site url", style="blue")
            table.add_column("username", style="magenta")
            table.add_column("email", style="green")
            table.add_column("password", style="red")

            for i in results:
                table.add_row(i[1], i[2], i[3], i[4], "********")
                console=Console()
                console.print(table)
                return
            
        if decrypt and len(results) == 1:
            mk=master_key(mp, ds)

            decrypted_password = utils.aesutil.decrypt(key=mk, source=results[0][5], keytype="bytes")
            print("[green][+][/green] password copied to clipboard")
            pyperclip.copy(decrypted_password.decode())
            return decrypted_password.decode()
        else:
            print("[green][+][/green] password copied to clipboard")
            pyperclip.copy(results[0][5])
            return results[0][5]    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()