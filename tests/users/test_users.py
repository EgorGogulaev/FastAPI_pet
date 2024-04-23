from sqlalchemy import select, insert

from users.models import User, Role
from conftest import sync_session_maker_test, async_session_maker_test


async def test_add_role():
    async with async_session_maker_test() as async_session:
        stmt = insert(Role).values(id=1, name="admin", permissions=None)
        await async_session.execute(stmt)
        await async_session.commit()
        
        query = select(Role)
        result = await async_session.execute(query)
        fetched_role = result.scalar()
        
        assert fetched_role, "Роль не была создана"


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
        query = select(User).where(User.email == "async_test@example.com")
        result = await async_session.execute(query)
        fetched_user = result.scalar()
        assert fetched_user, "Пользователь не был создан"
        

def test_sync_register(get_sync_client):
    response = get_sync_client.post(
        url="/auth/register",
        json={
            "email": "sync_test@example.com",
            "password": "sync_test",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False
        }
    )
        
    assert response.status_code == 201
    
    with sync_session_maker_test() as sync_session:
        query = select(User).where(User.email == "sync_test@example.com")
        result = sync_session.execute(query)
        fetched_user = result.scalar()
        assert fetched_user, "Пользователь не был создан"