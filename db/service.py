from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List, Type

from .models.Category import Category
from .models.Post import Post
from .models.PostLevel import PostLevel
from .schemas import *


def get_all_posts(db: Session, skip: int = 0, limit_posts: int = None):
    return db.query(Post).limit(100).all()


def get_post_by_id(db: Session, id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def get_post_by_category(db: Session, category_id: int):
    posts = db.query(Post.Post).filter(Post.Post.category_id == category_id).all()
    if posts is None:
        raise HTTPException(status_code=404, detail=f"Post not found with this category_id: {category_id}")
    return posts


def create_post(db: Session, post: PostSchema):
    if get_category_by_name(post.category_name):
        db_category = db.query(Category).filter(Category.name == post.category_name)
    else:
        db_category = create_category(db, post.category_name)

    db_post = Post(title=post.title, comments=post.comments, images_url=post.images_url, address=post.address,
                   category_id=db_category.id, level=post.level, votes=0)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_updated: PostUpdate, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.comments = post_updated.comments
    db_post.images_url = post_updated.images_url
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return "Post deletado"


def get_category_by_name(db: Session, name: str):
    db_category = db.query(Category).filter(Category.name == name).first
    return db_category is not None  # categoria com esse nome já existe


def create_category(db: Session, name: str):
    db_category = Category(name=name)
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
