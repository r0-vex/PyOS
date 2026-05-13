import secrets
import random
from hashlib import sha256

def hash_password(password):
    salt=secrets.token_hex(8)
    combined=password+salt
    hash_value=sha256(combined.encode()).hexdigest()
    return hash_value,salt

def verify_password(password,hash_value,salt):
    combined=password+salt
    return sha256(combined.encode()).hexdigest()==hash_value