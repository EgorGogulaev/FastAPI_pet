import pytest


from sqlalchemy import select, insert, update, delete

from users.models import User, Role
from conftest import async_session_maker_test, get_async_client


async def test_add_role():
    async with async_session_maker_test() as async_session:
        stmt = insert(Role).values(id=1, name="admin", permissions=None)
        await async_session.execute(stmt)
        await async_session.commit()
        
        query = select(Role)
        result = await async_session.execute(query)
        fetched_role = result.scalar()
        
        assert fetched_role, "Роль не была создана"

@pytest.mark.asyncio
async def test_async_register(get_async_client):
    response = await get_async_client.post(
        url="/auth/register",
        json={
            "email": "async_test@example.com",
            "password": "async_test",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False
        }
    )
    
    assert response.status_code == 201
    
    async with async_session_maker_test() as async_session:
        query = select(User)
        result = await async_session.execute(query)
        fetched_user = result.scalar()
        assert fetched_user, "Пользователь не был создан"
        

# def test_sync_register():
#     sync_client.post(
#         url="/auth/register",
#         json={
#             "email": "sync_test@example.com",
#             "password": "sync_test",
#             "is_active": True,
#             "is_superuser": False,
#             "is_verified": False
#         }
#     )