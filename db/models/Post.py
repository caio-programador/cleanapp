from sqlalchemy.orm import relationship
from sqlalchemy import Enum, Column, ForeignKey, Integer, String, ARRAY, Text

from .PostLevel import PostLevel
from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    comments = Column(Text)
    images_url = Column(Text)
    address = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    level = Column(Enum(PostLevel), index=True)
    likes = Column(Integer, index=True)

    category = relationship("Category")
