from passlib.context import CryptContext
import jwt
import uuid
from datetime import timedelta, datetime
from fastapi.exceptions import HTTPException
from fastapi import status

from src.config import Config



crypto = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

def hash_password(password:str)->str:
    return crypto.hash(secret=password, scheme='sha256_crypt')

def verify_password(password:str, hash:str)->bool:
    return crypto.verify(secret=password, hash=hash)

def create_jwt_token(user_data:dict, expire_delta:timedelta=timedelta(minutes=3), refresh:bool=False)->str:
    try:
        user_data['exp'] = (datetime.now() + expire_delta).timestamp()
        user_data['refresh'] = refresh
        user_data['jid'] = str(uuid.uuid4())
        return jwt.encode(payload=user_data, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGO)
    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='jwt token creation error')
    except Exception as e:
        raise Exception(f"JWT error {e}")

def verify_jwt_token(token:str):
    try:
        user_data = jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=Config.JWT_ALGO)
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='jwt token expired')
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='jwt invalid token')
    except jwt.exceptions.DecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='jwt decoding error')
    return user_data