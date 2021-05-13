# import required module
import base64
import os
import hashlib
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Get file hash
def hash_cert(fname):
    sha256_hash = hashlib.sha256()
    with open(fname, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def key_generation_fernet():
    # key generation which helps to cipher the information
    key = Fernet.generate_key()
    
    #save the key on the file
    with open('file.key', 'wb') as filekey:
        filekey.write(key)
    print('the key has been created')

def use_key(fname, pwd):
    kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length=32, salt=hash_cert(fname).encode(), iterations=10000)

    kname = base64.urlsafe_b64encode(kdf.derive(pwd.encode()))
    return kname

def encrypt_name_fernet(name, kname):
    #Using the key
    fernet = Fernet(kname)

    name_enc = fernet.encrypt(name)
    return name_enc

def decrypt_name_fernet(name, kname):
    #Usinfg the key
    fernet = Fernet(kname)
    name_dec = fernet.decrypt(name)
    return name_dec

def encrypt_file_fernet(fname, kname):
    # ENCRYPT THE FILE
    # read the file
    #with open(fname, 'rb') as filename:
    #    file_data = filename.read()

    #using the generated key
    fernet = Fernet(kname)

    #openning the file to be encrypt
    with open(fname, 'rb') as f:
        original = f.read()

    encrypted = fernet.encrypt(original)

    #opening the file in write mode and
    # write the encryted data
    with open(fname, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file_fernet(fname, kname):
    # Decrypt the encrypted file
    
    fernet = Fernet(kname)
    # opening the encrypted file
    with open(fname, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    #opening the file in write mode and writing the decrypted data
    with open(fname, 'wb') as dec_file:
        dec_file.write(decrypted)
