from beanie import Document
from typing import Dict
from datetime import datetime

from bson import ObjectId

from app.schemas.produto_schema import ProdutoSchema

class Servico(Document):
    solicitacao_id: str
    empresa_id: str
    prestador_id: str
    produto: ProdutoSchema  # Você pode tipar com Pydantic se quiser mais validação
    inicio: datetime
    previsao: datetime
    status: str = "Em andamento"

    class Settings:
        name = "servicos"