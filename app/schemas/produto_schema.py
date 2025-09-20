from typing import Optional
from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    nome: str
    quantidade: int
    detalhes: Optional[str] = None