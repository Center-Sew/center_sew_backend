from beanie import Document
from typing import Dict
from datetime import datetime

class Servico(Document):
    solicitacao_id: str
    empresa_id: str
    prestador_id: str
    produto: Dict  # Você pode tipar com Pydantic se quiser mais validação
    inicio: datetime
    previsao: datetime
    status: str = "em_andamento"

    class Settings:
        name = "servicos"