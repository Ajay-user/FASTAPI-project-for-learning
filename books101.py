from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

import aiofiles
import json
import pathlib
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book(BaseModel):
    id:int
    title:str
    author:str
    publisher:str
    publish_date:datetime
    page_count:int
    language:str

class BookUpdate(BaseModel):
    title:str
    author:str
    publisher:str
    publish_date:datetime
    page_count:int
    language:str

async def read_all_books():
    books_loc = pathlib.Path('./new_books.json')
    async with aiofiles.open(books_loc, mode='r') as fp:
        data = await fp.read()
    return json.loads(data) 

async def add_to_books(book:Book):
    # books_loc = pathlib.Path('./sample_book.json')
    data =  await read_all_books()
    book['publish_date'] = book['publish_date'].strftime('%Y-%m-%d')
    new_data = data + [book]
    async with aiofiles.open('./new_books.json', 'w') as fp:
        await fp.write(json.dumps(new_data))
    

@app.get(path='/', status_code=status.HTTP_200_OK, response_model=list[Book])
async def  get_all_books():
    data = await read_all_books()
    return data

@app.post(path='/create_book', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book:Book):
    book_to_append = book.model_dump()
    await add_to_books(book=book_to_append)
    return book_to_append

@app.patch(path='/update_book/{id}', status_code=status.HTTP_200_OK, response_model=BookUpdate)
async def patch_book(id:int, book:BookUpdate):
    book_details = book.model_dump()
    books = await get_all_books()
    books_updated = []
    item_no = None
    for i, item in enumerate(books):
        print(item)
        if item["id"] == id:
            item_no = i
            item['title'] = book_details['title']
            item['author'] = book_details['author']
            item['publish_date'] = book_details['publish_date'].strftime('%Y-%m-%d')
            item['page_count'] = book_details['page_count'] 
            item['language'] = book_details['language'] 
        books_updated.append(item)
    
    if item_no is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='id not found')
    else:
        async with aiofiles.open('./new_books.json', 'w') as fp:
            await fp.write(json.dumps(books_updated))

        return book_details
    

@app.delete(path='/delete_book/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def create_book(id:int):
    books = await get_all_books()

    updated_books = []
    item_no = None
    for i, book in enumerate(books):
        if id == book['id']:
            item_no = id
            continue
        updated_books.append(book)

    if item_no is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='id not found')
    else:
        async with aiofiles.open('./new_books.json', 'w') as fp:
            await fp.write(json.dumps(updated_books))
