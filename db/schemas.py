from pydantic import BaseModel
from typing import List
from db.models.PostLevel import PostLevel


class PostSchema(BaseModel):
    id: int
    title: str
    comments: List[str]
    images_url: List[str]
    latitude: float
    longitude: float
    level: PostLevel
    category_id: int
    likes: int

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    comments: List[str]
    latitude: float
    longitude: float
    level: PostLevel
    category_name: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    images_url: List[str]
    comments: List[str]

