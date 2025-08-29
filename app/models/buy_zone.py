from sqlalchemy import Column, Integer, Numeric, DateTime, String
from sqlalchemy.sql import func
from ..config.db import Base

class BuyZone(Base):
    __tablename__ = "buy_zone"

    id = Column(Integer, primary_key=True, index=True)
    buy_price = Column(Numeric(precision=18, scale=3))
    user = Column(String(100))
    create_at = Column(DateTime, server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}