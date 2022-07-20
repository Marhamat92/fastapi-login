from base_engine import Base
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB


class mUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(JSONB)
