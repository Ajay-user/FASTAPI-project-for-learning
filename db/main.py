from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker


from src.config import Config


from typing import AsyncGenerator

engine = AsyncEngine(sync_engine=create_engine(url=Config.DATABASE_URL, echo=True))

async def init_db():

    async with engine.begin() as conn:
        from src.Books.models import Book
        # This method allows traditional synchronous SQLAlchemy functions to run within the context of an asyncio application.
        await conn.run_sync(

            # Create all tables stored in this metadata.
            # Conditional by default, will not attempt to recreate tables already present in the target database.
            SQLModel.metadata.create_all
        )


    
async def get_session()->AsyncGenerator[AsyncSession, None]:
    # Construct a new .sessionmaker.
    Session =  sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    # Produce a new .Session object using the configuration
    # established in this .sessionmaker
    async with Session() as session:
        yield session