from ..database import Base
from sqlalchemy import Enum, Column, ForeignKey, Integer, String


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True)
