from pydantic import BaseModel
from datetime import datetime
import uuid

class Book(BaseModel):
    uid:uuid.UUID
    title:str
    author:str
    publisher:str
    publish_date:datetime
    page_count:int
    language:str
    created_at:datetime
    updated_at:datetime

class BookUpdate(BaseModel):
    title:str
    author:str
    publisher:str
    publish_date:datetime
    page_count:int
    language:str
