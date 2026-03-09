import secrets
import random
from hashlib import sha256

keys= ["<scK`8**s/","xUE-BtffUk","D1w^+M{VDZb"]

def hash_password(password):
    salt=secrets.token_hex(8)
    combined=password+salt
    hash_value=sha256(combined.encode()).hexdigest()
    return hash_value,salt

def verify_password(password,hash_value,salt):
    combined=password+salt
    return sha256(combined.encode()).hexdigest()==hash_value

def encrypt(data,key=None):
    if key is None:
        key = random.choice(keys)
    length_of_key=len(key)
    encrypted_data=""
    for i,letter in enumerate(repr(data)):
            letter_ascii,key_ascii=ord(letter),ord(key[i % length_of_key])
            encrypted_data+=chr(33+(letter_ascii+key_ascii-33)%94)
    if key not in keys:
         return repr(encrypted_data)
    return [repr(encrypted_data),keys.index(key)]

def decrypt(data,key):
    length_of_key=len(key)
    decrypted_data=""
    for i,letter in enumerate(repr(data)):
        letter_ascii,key_ascii=ord(letter),ord(key[i % length_of_key])
        decrypted_data+=chr(33+(letter_ascii-key_ascii-33)%94)
    return repr(decrypted_data)