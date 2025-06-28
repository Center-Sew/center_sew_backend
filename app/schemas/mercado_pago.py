from pydantic import BaseModel, Field
from typing import Optional, Dict

class MetadataSchema(BaseModel):
    user_id: str
    plano_id: str
    plano_nome: Optional[str]
    plano_valor: Optional[float]
    tipo_usuario: Optional[str]

class PagamentoDetalhesSchema(BaseModel):
    id: int
    status: str
    status_detail: Optional[str]
    metadata: MetadataSchema
