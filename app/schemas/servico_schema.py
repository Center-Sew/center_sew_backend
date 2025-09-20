from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer

from app.schemas.produto_schema import ProdutoSchema
from app.schemas.usuario_schema import UsuarioResponse  # ← nova importação

class ServicoCreate(BaseModel):
    solicitacao_id: str
    empresa_id: str
    prestador_id: str
    produto: ProdutoSchema
    inicio: datetime
    previsao: datetime

class ServicoResponse(ServicoCreate):
    id: str = Field(alias="_id")
    status: str
    titulo_solicitacao: Optional[str] = None
    empresa: UsuarioResponse
    prestador: UsuarioResponse

    @field_serializer('id')
    def serialize_object_id(self, value: ObjectId, _info):
        return str(value)

    class Config:
        validate_by_name = True
        from_attributes = True