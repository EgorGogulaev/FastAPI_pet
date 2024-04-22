from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import Operation
from .schemas import OperationCreate


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

# ВАЖНО! В лог и сообщении об ошибке можно включить uuid для легкого отслеживания произошедшего события

@router.get("/")
async def get_all_operations(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation)
        result = await session.execute(query).all()
        return {
            "status": True,
            "msg": "Успешно",
            "data": result
        }
    except Exception as ex:
        print(ex)  # тут должна быть запись лога
        return {
            "status": False,
            "msg": "Что-то пошло не так",
        }

@router.get("/specific")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.execute(query).all()
        return {
            "status": True,
            "msg": "Успешно",
            "data": result
        }
    except Exception as ex:
        print(ex)  # тут должна быть запись лога
        return {
            "status": False,
            "msg": "Что-то пошло не так",
        }
    

@router.post("/specific")
async def add_specific_operations(new_operations: List[OperationCreate], session: AsyncSession = Depends(get_async_session)):
    try:
        data = [Operation(**i.model_dump()) for i in new_operations]  # проходимся по списку добавляемых операций, преобразуем в словарь и раскрываем в объект модели для последующего добавления в сессию
        await session.add_all(data)
        await session.commit()
        
        return {
            "status": True,
            "msg": "Успешно"
        }
    except Exception as ex:
        print(ex)  # тут должна быть запись лога
        return {
            "status": False,
            "msg": "Что-то пошло не так"
        }
