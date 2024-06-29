from fastapi import FastAPI, Depends
import uvicorn

from db.database import Base, engine
from dependencies import get_db
from routers import posts, categories

Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(posts.router)
app.include_router(categories.router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
