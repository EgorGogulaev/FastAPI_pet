import asyncio
import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from database import get_async_session
from .config import get_user_db, get_user_manager
from .schemas import UserCreate


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")



if __name__ == "__main__":
    email = "example@mail.ru"
    password = "some_password"
    
    asyncio.run(create_user(email=email, password=password, is_superuser=False))
