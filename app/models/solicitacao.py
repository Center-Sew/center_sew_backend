from datetime import datetime
from typing import List
from beanie import Document
from pydantic import Field

from app.models.perfil_desejado import PerfilDesejado


class Solicitacao(Document):
    titulo: str
    descricao: str
    empresa_id: str
    perfil_desejado: PerfilDesejado
    status: str = "aberta"
    data_criacao: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    interessados: List[str] = []

    class Settings:
        name = "solicitacoes"