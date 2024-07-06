from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# INICIE AQUI: Este arquivo fará a a conexão com o banco de dados
# Configuramos qual Banco de dados usar e onde ele se encontra

SQLALCHEMY_DATABASE_URL = "sqlite:///./cleanapp.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
