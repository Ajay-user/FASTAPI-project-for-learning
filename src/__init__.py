from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.Books.router import book_router
from db.main import init_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("BEFORE")
    result = await init_db()
    print(result)

    yield

    print("AFTER")


version = 'v1'
app = FastAPI(
    version=version,
    description="A Book details REST API",
    title="BooksAPI",
    lifespan=lifespan
)


app.include_router(router=book_router, prefix=f"/api/{version}/books", tags=['books'])