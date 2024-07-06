import os
from datetime import datetime
from typing import List
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form

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

MAPS_API_KEY = "AIzaSyBJ9g92euQMzv3ac0zaxYi4yYROVlFRnwA"


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
def create_post_router(
        title: str = Form(...),
        comments: List[str] = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        category_name: str = Form(...),
        post_level: PostLevel = Form(...),
        db: Session = Depends(get_db),
        files: List[UploadFile] = File(...)
):
    post = PostCreate(
        title=title,
        comments=comments,
        latitude=latitude,
        longitude=longitude,
        level=post_level,
        category_name=category_name
    )

    images_url = []
    for file in files:
        file_path = save_image(file)
        images_url.append(file_path)

    return create_post(db, post, images_url)


def save_image(file: UploadFile) -> str:
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    # Criar caminho dos diretórios
    dir_path = os.path.join("media", year, month, day)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


@router.put("/{id}", response_model=PostSchema)
def update_post_router(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    return update_post(db, post, id)


@router.delete("/{id}")
def delete_post_router(id: int, db: Session = Depends(get_db)):
    return delete_post(db, id)


@router.post("/like/{id}")
def liking_post(id: int, db: Session = Depends(get_db)):
    post_likes(db, id)
    return "CURTIDASSO"
