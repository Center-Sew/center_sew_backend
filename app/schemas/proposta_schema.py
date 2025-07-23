from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

from app.schemas.solicitacao_schema import UsuarioSlim

class PropostaCreate(BaseModel):
    mensagem: str
    valor: Optional[float] = None

class PropostaModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    solicitacao_id: str
    usuario_id: str
    empresa_id: str
    mensagem: str
    data_envio: datetime
    status: str
    usuario: Optional[UsuarioSlim] = None
    possui_mensagem_nova: bool = False

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
    }