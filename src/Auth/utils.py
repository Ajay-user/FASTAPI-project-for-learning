from passlib.context import CryptContext


crypto = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

def hash_password(password:str)->str:
    return crypto.hash(secret=password, scheme='sha256_crypt')

def verify_password(password:str, hash:str)->bool:
    return crypto.verify(secret=password, hash=hash)