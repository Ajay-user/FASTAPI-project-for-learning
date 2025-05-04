from passlib.context import CryptContext
import jwt
from datetime import timedelta

from src.config import Config



crypto = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

def hash_password(password:str)->str:
    return crypto.hash(secret=password, scheme='sha256_crypt')

def verify_password(password:str, hash:str)->bool:
    return crypto.verify(secret=password, hash=hash)

def create_jwt_token(user_data:dict, expire_delta:timedelta=timedelta(seconds=30))->str:
    try:
        return  jwt.encode(payload=user_data, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGO)
    except jwt.exceptions.PyJWTError as e:
        raise Exception(f"JWT error : {e}")

def verify_jwt_token(token:str):
    try:
        user_data = jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=Config.JWT_ALGO)
        return user_data
    except jwt.exceptions.DecodeError as e:
        raise Exception(f'JWT decode exeception: {e}')
    except jwt.exceptions.ExpiredSignatureError as e:
        raise Exception(f'JWT token expired: {e}')