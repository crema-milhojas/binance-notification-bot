from sqlalchemy import Column, Integer, Numeric, DateTime, String
from sqlalchemy.sql import func
from ..config.db import Base

class ArbitrationUstd(Base):
    __tablename__ = "arbitration_ustd"

    id = Column(Integer, primary_key=True, index=True)
    trans_amount = Column(Numeric(precision=18, scale=3))
    buy_price = Column(Numeric(precision=18, scale=3))
    buyer_nickname = Column(String(100)) 
    sell_price = Column(Numeric(precision=18, scale=3))
    seller_nickname = Column(String(100)) 
    spread = Column(Numeric(precision=18, scale=3))
    create_at = Column(DateTime, server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}