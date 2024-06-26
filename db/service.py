from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List, Type

from .models import Category, Post
from .models.PostLevel import PostLevel
from .schemas import *


def get_all_posts(db: Session, skip: int = 0, limit_posts: int = None) -> List[Post.Post]:
    return db.query(Post.Post).limit(100).all()


def get_post_by_id(db: Session, id: int) -> Post.Post:
    post = db.query(Post.Post).filter(Post.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def get_post_by_category(db: Session, category_id: int) -> List[Post.Post]:
    posts = db.query(Post.Post).filter(Post.Post.category_id == category_id).all()
    if posts is None:
        raise HTTPException(status_code=404,detail=f"Post not found with this category_id: {category_id}")
    return posts


def create_post(db: Session, post: PostSchema):
    db_post = Post.Post(title=post.title, comments=post.comments, images_url=post.images_url, address=post.address,
                        category_id =0, level=post.level, votes=0)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_updated: PostUpdate, id: int):
    db_post = db.query(Post.Post).filter(Post.Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.comments = post_updated.comments
    db_post.images_url = post_updated.images_url
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, id: int):
    db_post = db.query(Post.Post).filter(Post.Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return "Post deletado"
