from beanie import Document
from pydantic import Field

class Plano(Document):
    nome: str
    descricao: str
    icone: str
    preco: str
    validade: str

    class Settings:
        name = "planos"