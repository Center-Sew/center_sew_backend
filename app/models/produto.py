from beanie import Document
from typing import Optional

class Produto(Document):
    nome: str
    quantidade: int
    detalhes: Optional[str] = None

    class Settings:
        name = "produtos"