from datetime import datetime, timezone
from beanie import Document
from pydantic import Field

class Proposta(Document):
    solicitacao_id: str           # FK -> Solicitacao._id
    prestador_id: str             # FK -> Usuario._id
    mensagem: str                 # máx 500 caracteres
    data_envio: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(default="pendente")  # pendente | aceita | recusada

    class Settings:
        name = "propostas"