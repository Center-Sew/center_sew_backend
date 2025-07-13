from datetime import datetime, timezone
from typing import List, Optional
from beanie import Document
from pydantic import Field

from app.models.perfil_desejado import PerfilDesejado


class Solicitacao(Document):
    titulo: str
    descricao: str
    empresa_id: str
    perfil_desejado: PerfilDesejado
    status: str = "aberta"
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    interessados: int
    imagens: Optional[List[str]] = []

    class Settings:
        name = "solicitacoes"