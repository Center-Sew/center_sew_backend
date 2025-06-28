# app/schemas/pagamento_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict
from app.schemas.base import BaseModelWithStrObjectId

class PagamentoCreate(BaseModel):
    id_pagamento: int
    status: str
    status_detail: Optional[str]
    descricao: str
    valor: float
    metodo_pagamento: Optional[str]
    tipo_pagamento: Optional[str]
    data_criacao: datetime = Field(default_factory=datetime.utcnow)

    user_id: str
    tipo_usuario: str
    plano_id: str
    plano_nome: str
    plano_valor: float

    payload_completo: Optional[Dict] = None

class PagamentoModel(BaseModelWithStrObjectId, PagamentoCreate):
    pass