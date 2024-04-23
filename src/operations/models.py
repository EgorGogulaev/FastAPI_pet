from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Operation(Base):
    __tablename__ = 'operation'
    
    id = Column(BigInteger, primary_key=True)
    
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=False)
    type = Column(String)
    operation_datetime = Column(DateTime(timezone=False))
    create_at = Column(DateTime(timezone=False), server_default=func.now())