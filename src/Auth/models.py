from sqlmodel import SQLModel, Column, Field
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


'''

In SQLModel, the exclude=True parameter in the Field function for the password field indicates 
that this field should be excluded when serializing the model into dictionaries or JSON. 
Essentially, this prevents the password from being included in operations where the model is converted into a dictionary, 
ensuring sensitive information like passwords aren’t unintentionally exposed.

user = User(username="example", email="example@email.com", password="securepassword")
print(user.dict())

The output will not contain the password field because it has been excluded from serialization.

'''
class User(SQLModel, table=True):
    __tablename__='user' 
    uid:uuid.UUID = Field(sa_column=Column(type_=pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4))
    username:str
    email:str
    password:str=Field(exclude=True)
    first_name:str
    last_name:str
    is_verified:bool = False
    created_at:datetime = Field(sa_column=Column(type_=pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(type_=pg.TIMESTAMP, default=datetime.now))