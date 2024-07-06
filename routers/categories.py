from typing import List
from fastapi import APIRouter, Depends

from db.models.Category import Category

from db.service import *
from dependencies import get_db
from sqlalchemy.orm import Session

# INICIE AQUI: configuração de rota da categoria
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)


# Rota que retorna todas as categorias
@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()