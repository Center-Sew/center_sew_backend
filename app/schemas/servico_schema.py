from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ProdutoSchema(BaseModel):
    nome: str
    quantidade: int
    detalhes: Optional[str] = None

class ServicoCreate(BaseModel):
    solicitacao_id: str
    prestador_id: str
    produto: ProdutoSchema
    inicio: datetime
    previsao: datetime

class ServicoResponse(ServicoCreate):
    id: str = Field(alias="_id")
    empresa_id: str
    status: str

    class Config:
        validate_by_name = True
        from_attributes = True