from typing import List
from fastapi import APIRouter, Depends

from db.models.Post import Post

from db.service import *
from dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)