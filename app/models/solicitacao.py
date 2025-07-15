from datetime import datetime, timezone
from typing import List, Optional
from beanie import Document
from pydantic import Field
from bson import ObjectId

from app.models.perfil_desejado import PerfilDesejado

class Solicitacao(Document):
    titulo: str
    descricao: str
    usuario_id: ObjectId  # Substitui empresa_id
    perfil_desejado: PerfilDesejado
    status: str = "aberta"
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    interessados: int = 0
    imagens: Optional[List[str]] = []

    class Settings:
        name = "solicitacoes"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }