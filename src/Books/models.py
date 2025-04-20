from sqlmodel import SQLModel, Column, Field
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class Book(SQLModel, table=True):
    __tablename__ = 'books'
    uid:uuid.UUID = Field(sa_column=Column(type_=pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    title:str
    author:str
    publisher:str
    publish_date:datetime = Field(sa_column=Column(type_=pg.TIMESTAMP))
    page_count:int
    language:str
    created_at:datetime = Field(sa_column=Column(type_=pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(type_=pg.TIMESTAMP, default=datetime.now))

    # def __repr__(self):
    #     return f"<BOOK {self.title}>"
