
import pathlib
import aiofiles
import json
from typing import Sequence

from fastapi.security import HTTPAuthorizationCredentials
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio.session import AsyncSession


from src.Auth.dependency import AccessTokenHandler
from src.Books.schema import Book, BookUpdate
from src.Books.services import BookService
from db.main import get_session



book_router = APIRouter()
book_service = BookService()
access_token = AccessTokenHandler()
    

@book_router.get(path='/', status_code=status.HTTP_200_OK, response_model=Sequence[Book])
async def  get_all_books(session:AsyncSession=Depends(dependency=get_session), security:HTTPAuthorizationCredentials=Depends(access_token)):
    data = await book_service.get_all_books(session=session)
    return data

@book_router.get(path='/{id}', status_code=status.HTTP_200_OK, response_model=Book)
async def get_book(id:str,  session:AsyncSession=Depends(dependency=get_session)):
    data = await book_service.get_book(uid=id, session=session)
    return data

@book_router.post(path='/create_book', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book:BookUpdate, session:AsyncSession=Depends(get_session)):
    book = await book_service.create_book(book=book, session=session)
    return book

@book_router.patch(path='/update_book/{id}', status_code=status.HTTP_200_OK, response_model=Book)
async def patch_book(id:str, book:BookUpdate, session:AsyncSession=Depends(dependency=get_session)):

    book = await book_service.update_book(uid=id, book=book, session=session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='id not found')
    

@book_router.delete(path='/delete_book/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def create_book(id:str, session:AsyncSession=Depends(dependency=get_session)):
    book = await book_service.delete_book(uid=id, session=session)
    if book is None:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='id not found')
