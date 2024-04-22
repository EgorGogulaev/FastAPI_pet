from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTable
)
from sqlalchemy import Column, String, SmallInteger, Integer, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, declared_attr, mapped_column, Mapped


Base = declarative_base()


class User(SQLAlchemyBaseUserTable, Base):
    id = Column(Integer, primary_key=True)
    
    # Опциональная настройка доп. полей
    role_id = Column(SmallInteger, ForeignKey("role.id", onupdate="CASCADE", ondelete="CASCADE"))
    

class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)

class Role(Base):
    __tablename__ = "role"
    
    id = Column(SmallInteger, primary_key=True)
    
    name = Column(String, nullable=False)
    permissions = Column(JSON)
