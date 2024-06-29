from typing import List
from fastapi import APIRouter, Depends

from db.models.Post import Post

from db.service import *
from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[PostSchema])
def get_all_router(db: Session = Depends(get_db)) -> List[PostSchema]:
    return get_all_posts(db)


@router.get("/{id}", response_model=PostSchema)
def get_post_by_id_router(id: int, db: Session = Depends(get_db)) -> PostSchema:
    return get_post_by_id(db, id)


@router.get("/categories/{category_id}")
def get_post_by_category_id_router(category_id: int, db: Session = Depends(get_db)) -> PostSchema:
    return get_post_by_category(db, category_id)


@router.post("/", response_model=PostSchema)
def create_post_router(post: PostSchema, db: Session = Depends(get_db)):
    return create_post(db, post)


@router.put("/{id}")
def update_post_router(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    return update_post(db, post, id)


@router.delete("/{id}")
def delete_post_router(id: int, db: Session = Depends(get_db)):
    return delete_post(db, id)


@router.post("/like/{id}")
def liking_post(id: int, db: Session = Depends(get_db)):
    post_likes(db, id)
    return "CURTIDASSO"
