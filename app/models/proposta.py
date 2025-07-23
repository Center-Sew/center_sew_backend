from datetime import datetime, timezone
from typing import Annotated, Optional

from beanie import Document
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId

from app.schemas.solicitacao_schema import UsuarioSlim

# Conversor para aceitar ObjectId no input e serializar como string no output
PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]

class Proposta(Document):
    solicitacao_id: ObjectId           # FK -> Solicitacao._id
    usuario_id: ObjectId               # FK -> Usuario._id (prestador)
    empresa_id: ObjectId               # FK -> Usuario._id (empresa)
    mensagem: str = Field(..., max_length=500)
    data_envio: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(default="pendente")  # pendente | aceita | recusada

    class Settings:
        name = "propostas"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
    }

# Schema de resposta (usado em APIs para evitar erro de validação)
class PropostaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    solicitacao_id: PyObjectId
    usuario_id: PyObjectId
    empresa_id: PyObjectId
    mensagem: str
    data_envio: Optional[datetime] = None
    status: Optional[str] = None
    usuario: Optional[UsuarioSlim] = None

    class Config:
        populate_by_name = True