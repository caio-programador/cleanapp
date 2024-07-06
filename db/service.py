import json

from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List

from .models.Category import Category
from .models.Post import Post
from .models.PostLevel import PostLevel
from .schemas import *


# INICIE AQUI: neste arquivo se encontram as funções por conectar as rotas e o banco de dados


# Função que pega todos os posts do banco de dados e os retorna
def get_all_posts(db: Session, skip: int = 0, limit_posts: int = 100) -> List[PostReturn]:
    posts = db.query(Post).offset(skip).limit(limit_posts).all()
    return [convert_post_schemas(post) for post in posts]


# Pega um post com base no id
def get_post_by_id(db: Session, id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return convert_post_schemas(post)


# Função que retorna uma lista de posts com base no id da categoria
def get_post_by_category(db: Session, category_id: int):
    posts = db.query(Post.Post).filter(Post.Post.category_id == category_id).all()
    if posts is None:
        raise HTTPException(status_code=404, detail=f"Post not found with this category_id: {category_id}")
    return posts


# Função que cria o post
def create_post(db: Session, post: PostCreate, images_url: List[str]):
    # Verifica se a categoria existe, caso contrário, cria uma nova
    db_category = get_category_by_name(db, post.category_name)
    if db_category is None:
        db_category = create_category(db, post.category_name)

    # Converte comments e images_url para JSON
    json_images_url = json.dumps(images_url)

    # Cria o objeto Post
    db_post = Post(
        title=post.title,
        description=post.description,
        images_url=json_images_url,
        latitude=post.latitude,
        longitude=post.longitude,
        category_id=db_category.id,
        level=post.level,
        likes=0
    )
    # Adiciona e confirma a transação
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return convert_post_schemas(db_post)


# Função que exclui um post
def delete_post(db: Session, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return "Post deletado"


# Função que procura por uma categoria no banco de dados para verificar a existência
def get_category_by_name(db: Session, name: str):
    db_category = db.query(Category).filter(Category.name == name).first()
    return db_category


# Função que cria uma nova categoria
def create_category(db: Session, name_category: str):
    db_category = Category(name=name_category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Função que incrementa as curtidas de um post
def post_likes(db: Session, id: int):
    db_post = db.query(Post).filter(Post.id == id).first()
    db_post.likes += 1
    db.commit()
    db.refresh(db_post)


# Função que retorna todas as categorias
def get_all_categories(db: Session):
    return db.query(Category).all()


# Função que converte o que vem do banco de dados para um objeto que as rotas consigam entender e entregar
def convert_post_schemas(post: Post) -> PostReturn:
    return PostReturn(
        id=post.id,
        title=post.title,
        description=post.description,  # converte string para lista (loads())
        images_url=json.loads(post.images_url),
        latitude=post.latitude,
        longitude=post.longitude,
        level=post.level,
        category_id=post.category_id,
        likes=post.likes,
    )
