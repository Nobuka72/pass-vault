import base64
from Crypto.Cipher import AES
import secrets
import sys

def encryptor(key, source, encode=True, keytype='hex'):
    source = source.encode()
    if keytype == 'hex':
        key = bytes(bytearray.fromhex(key))
    IV = secrets.token_bytes(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - (len(source) % AES.block_size)
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source)
    if encode:
        return base64.b64encode(data).decode()
    return data

def decryptor(key, source, decode=True, keytype='hex'):
    source= source.encode()
    if decode:
        source = base64.b64decode(source)
    if keytype == 'hex':
        key = bytes(bytearray.fromhex(key))
    IV= source[:AES.block_size]
    decryptor= AES.new(key, AES.MODE_CBC, IV)
    data= decryptor.decrypt(source[AES.block_size:])
    padding= data[-1]
    if data[-padding:] != bytes([padding])*padding:
        print("Invalid padding...")
        sys.exit(1)
    return data[:-padding].decode()