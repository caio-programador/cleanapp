from fastapi import FastAPI, Depends
import uvicorn

from db.database import Base, engine
from dependencies import get_db
from routers import posts, categories

# Cria o banco de dados
Base.metadata.create_all(bind=engine)

# Instancia a aplicação do FAST
app = FastAPI(dependencies=[Depends(get_db)])

# Inclui as rotas/caminhos para a API
app.include_router(posts.router)
app.include_router(categories.router)

# Roda o código
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)