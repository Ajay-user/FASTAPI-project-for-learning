from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get(path='/')
async def read_root():
    return {"message": "hello world"}

# url path has a param
# @app.get(path='/greet/{name}')
# async def greet_name(name:str)->dict:
#     return {"message": f"hello {name}"}

# query parameter
# @app.get(path='/greet')
# async def greet_name(name:str)->dict:
#     return {"message": f"hello {name}"}


# optional query params
@app.get(path='/greet')
async def greet_name(name:Optional[str]='Ajay')->dict:
    return {"message": f"hello {name}"}



# POST req schema

class BookCreateModel(BaseModel):
    title:str 
    author:str


@app.post('/create_book')
async def create_book(book_data:BookCreateModel):
    return{
        'title' : book_data.title,
        'author' : book_data.author
    }


# get header info

@app.get('/get_header_info')
async def get_header_info(
    accept:str=Header(default=None), content_type:str=Header(default=None),
    user_agent:str=Header(default=None), host:str=Header(default=None)
    ):
    headers = {}
    headers['Accept'] = accept
    headers['Content-Type'] = content_type
    headers['User-Agent'] = user_agent
    headers['Host'] = host

    return headers