
import pytest
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.main import app
from src.database import get_sync_session, get_async_session
from src.operations.models import Base as operations_base
from src.users.models import Base as users_base
from src.config import test_db_user, test_db_pass, test_db_host, test_db_port, test_db_name


DATABASE_URL_async_test = f"postgresql+asyncpg://{test_db_user}:{test_db_pass}@{test_db_host}:{test_db_port}/{test_db_name}"

async_engine_test = create_async_engine(DATABASE_URL_async_test)
async_session_maker_test = async_sessionmaker(async_engine_test, class_=AsyncSession, expire_on_commit=True)
operations_base.metadata.bind = async_engine_test
users_base.metadata.bind = async_engine_test


@asynccontextmanager
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


# НАСТРОЙКА РАБОТЫ С ТЕСТОВЫМИ КЛИЕНТАМИ
# Создание fixture для инициализации схемы в тестовой базе данных с последующим удалением после выполнения тестов
@pytest.fixture(autouse=True, scope="session")
async def prepare_test_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(operations_base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(operations_base.metadata.drop_all)

sync_client = TestClient(app=app)  # создание тестового синхронного клиента

# Создание тестового асинхронного клиента
@pytest.fixture(scope="session")
async def get_async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client

