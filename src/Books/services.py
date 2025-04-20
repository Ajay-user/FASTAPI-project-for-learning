from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc


from .models import Book as BookModel
from .schema import Book, BookUpdate

import uuid
from typing import Sequence


class BookService:

    async def get_all_books(self, session:AsyncSession)->Sequence[Book]:
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        # result = await session.exec(statement=statement)
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_book(self, uid:uuid.UUID, session:AsyncSession)->Book|None:
        statement = select(BookModel).where(BookModel.uid == uid)
        result = await session.execute(statement=statement)
        # print("RAW >>>>>>>>>>>>>>>>", result.scalar())
        # Fetch the first object or None if no object is present.
        return result.scalar()

    async def create_book(self, book:BookUpdate, session:AsyncSession)->Book:
        book_dict = book.model_dump()
        book_to_create = BookModel(**book_dict)
        session.add(book_to_create)
        await session.commit()
        return book_to_create

    async def update_book(self, uid:uuid.UUID, book:BookUpdate, session:AsyncSession)->Book|None:
        book_dict = book.model_dump()
        book_to_update = await self.get_book(uid=uid, session=session)
        if book_to_update:
            for k,v in book_dict.items():
                setattr(book_to_update, k, v)
            session.add(book_to_update)
            await session.commit()

        return book_to_update

    async def delete_book(self, uid:uuid.UUID, session:AsyncSession)->Book|None:
        book_to_delete = await self.get_book(uid=uid, session=session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
        return book_to_delete
        