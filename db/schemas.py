from pydantic import BaseModel
from typing import List
from db.models.PostLevel import PostLevel


# INICIE AQUI: Este arquivo possui os objetos que serão retornados ou usados pelas rotas

class PostReturn(BaseModel):
    id: int
    title: str
    description: str
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
    description: str
    latitude: float
    longitude: float
    level: PostLevel
    category_name: str

    class Config:
        from_attributes = True



