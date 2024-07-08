import os
from datetime import datetime
from typing import List
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form

from db.models.Post import Post

from db.service import *
from dependencies import get_db
from sqlalchemy.orm import Session

# Configuração da rota post, terá o caminho padrão + "/posts"
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)


# Rota que retorna todos os posts no banco de dados
@router.get("/", response_model=List[PostReturn])
def get_all_router(db: Session = Depends(get_db)) -> List[PostReturn]:
    return get_all_posts(db)


# Rota que retorna apenas um post do banco de dados
@router.get("/{id}", response_model=PostReturn)
def get_post_by_id_router(id: int, db: Session = Depends(get_db)) -> PostReturn:
    return get_post_by_id(db, id)


# rota que retorna uma lista de posts conforme o id de sua categoria
@router.get("/categories/{category_id}")
def get_post_by_category_id_router(category_id: int, db: Session = Depends(get_db)) -> PostReturn:
    return get_post_by_category(db, category_id)


# rota que cria um post no banco de dados e retorna o mesmo
@router.post("/", response_model=PostReturn)
def create_post_router(
        title: str = Form(...),
        description: str = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        category_name: str = Form(...),
        post_level: PostLevel = Form(...),
        db: Session = Depends(get_db),
        files: List[UploadFile] = File(...)
):
    post = PostCreate(
        title=title,
        description=description,
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


# Função para salvar a imagem em uma pasta media dentro diretório do projeto
def save_image(file: UploadFile) -> str:
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    # Criar caminho dos diretórios
    dir_path = os.path.join("media", year, month, day)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, file.filename)

    file_path.replace("\\", "/")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# Rota para deletar um problema em caso de erro
@router.delete("/{id}")
def delete_post_router(id: int, db: Session = Depends(get_db)):
    return delete_post(db, id)


# Rota para incrementar um like em um post
@router.post("/like/{id}")
def liking_post(id: int, db: Session = Depends(get_db)):
    post_likes(db, id)
