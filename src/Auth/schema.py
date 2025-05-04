from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing_extensions import Optional
import uuid



class User(BaseModel):
    uid:uuid.UUID
    email:EmailStr
    password:str = Field(exclude=True)
    first_name:str
    last_name:str
    is_verified:bool = False
    created_at:datetime
    updated_at:datetime



class CreateUser(BaseModel):
    username:str
    email:EmailStr
    password:str
    first_name:str
    last_name:str
    is_verified:bool = False


class UserCred(BaseModel):
    email:EmailStr
    password:str