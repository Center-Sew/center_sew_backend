from pydantic import BaseModel, Field
from app.schemas.base import BaseModelWithStrObjectId

class PlanoCreate(BaseModel):
    nome: str
    descricao: str
    icone: str
    preco: str
    validade: str

class PlanoModel(BaseModelWithStrObjectId, PlanoCreate):
    pass