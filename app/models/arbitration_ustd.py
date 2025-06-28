from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.sql import func
from ..config.db import Base

class ArbitrationUstd(Base):
    __tablename__ = "arbitration_ustd"

    id = Column(Integer, primary_key=True, index=True)
    trans_amount = Column(Numeric(precision=18, scale=2))
    buy_price = Column(Numeric(precision=18, scale=2))
    sell_price = Column(Numeric(precision=18, scale=2))
    spread = Column(Numeric(precision=18, scale=2))
    createAt = Column(DateTime, server_default=func.now())