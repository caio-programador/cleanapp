from pydantic import BaseModel
from db.models.PostLevel import PostLevel


class PostSchema(BaseModel):
    id: int
    title: str
    comments: str
    images_url: str
    address: str
    level: PostLevel
    category_id: int

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    comments: List[str]
    images_url: List[str]
    address: str
    level: PostLevel
    category_name: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    images_url: str
    comments: str


class PostVotes(BaseModel):
    votes: int
