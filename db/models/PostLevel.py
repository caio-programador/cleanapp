from enum import Enum


# Tipo enumerado para separar e limitar a gravidade de um problema
class PostLevel(Enum):
    ALTO = "Alto"
    MEDIO = "Médio"
    BAIXO = "Baixo"
