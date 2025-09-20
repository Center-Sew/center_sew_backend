# app/models/proposta_model.py
from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field
from bson import ObjectId

from app.schemas.chat_schema import PyObjectId
from app.schemas.solicitacao_schema import UsuarioSlim

class Proposta(Document):
    solicitacao_id: ObjectId           # FK -> Solicitacao._id
    prestador_id: ObjectId             # FK -> Usuario._id (prestador)  <-- RENOMEADO
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