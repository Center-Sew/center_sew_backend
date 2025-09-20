# app/models/solicitacao.py
from datetime import datetime, timezone
from typing import List, Optional
from beanie import Document, Indexed
from pydantic import Field
from bson import ObjectId

from app.models.perfil_desejado import PerfilDesejado

class Solicitacao(Document):
    titulo: str
    descricao: str
    usuario_id: ObjectId  # empresa/usuário dono
    perfil_desejado: PerfilDesejado

    status: str = "aberta"
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # ⬇️ NOVO: data prevista em UTC, indexada
    data_prevista_entrega: Optional[datetime] = Indexed(None)

    interessados: int = 0
    imagens: Optional[List[str]] = []
    proposta_aceita: bool = False

    class Settings:
        name = "solicitacoes"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
