from contextlib import asynccontextmanager
from typing import Generator, AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession 

from src.config import db_user, db_pass, db_host, db_port, db_name

DATABASE_URL_sync = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
DATABASE_URL_async = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

sync_engine = create_engine(DATABASE_URL_sync)
async_engine = create_async_engine(DATABASE_URL_async)

sync_session_maker = sessionmaker(sync_engine)
async_session_maker = async_sessionmaker(async_engine)

def get_sync_session() -> Generator[Session, None, None]:
    with sync_session_maker() as session:
        yield session 

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
