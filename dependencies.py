from db.database import SessionLocal


# Dependência para a conexão com o banco de dados
# Obriga que para funcionar as rotas se conecte com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
