import json

from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List

from .models.Category import Category
from .models.Post import Post
from .models.PostLevel import PostLevel
from .schemas import *


def get_all_posts(db: Session, skip: int = 0, limit_posts: int = 100) -> List[PostSchema]:
    posts = db.query(Post).offset(skip).limit(limit_posts).all()
    return [convert_post_schemas(post) for post in posts]


def get_post_by_id(db: Session, id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return convert_post_schemas(post)


def get_post_by_category(db: Session, category_id: int):
    posts = db.query(Post.Post).filter(Post.Post.category_id == category_id).all()
    if posts is None:
        raise HTTPException(status_code=404, detail=f"Post not found with this category_id: {category_id}")
    return posts


def create_post(db: Session, post: PostCreate):
    # Verifica se a categoria existe, caso contrário, cria uma nova
    db_category = get_category_by_name(db, post.category_name)
    if db_category is None:
        db_category = create_category(db, post.category_name)

    # Converte comments e images_url para JSON
    json_comments = json.dumps(post.comments)
    json_images_url = json.dumps(post.images_url)

    # Cria o objeto Post
    db_post = Post(
        title=post.title,
        comments=json_comments,
        images_url=json_images_url,
        address=post.address,
        category_id=db_category.id,
        level=post.level,
        likes=0
    )
    # Adiciona e confirma a transação
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return convert_post_schemas(db_post)


def update_post(db: Session, post_updated: PostUpdate, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.comments = post_updated.comments
    db_post.images_url = post_updated.images_url
    db.commit()
    db.refresh(db_post)
    return convert_post_schemas(db_post)


def delete_post(db: Session, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return "Post deletado"


def get_category_by_name(db: Session, name: str):
    db_category = db.query(Category).filter(Category.name == name).first()
    return db_category


def create_category(db: Session, name_category: str):
    db_category = Category(name=name_category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def post_likes(db: Session, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    db_post.likes += 1
    db.commit()
    db.refresh(db_post)


def get_all_categories(db: Session):
    return db.query(Category).all()


def convert_post_schemas(post: Post) -> PostSchema:
    return PostSchema(
        id=post.id,
        title=post.title,
        comments=json.loads(post.comments),  # converte string para lista (loads())
        images_url=json.loads(post.images_url),
        address=post.address,
        level=post.level,
        category_id=post.category_id
    )
