from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.base import BaseModelWithStrObjectId

class PropostaCreate(BaseModel):
    mensagem: str = Field(..., max_length=500)

class PropostaModel(BaseModelWithStrObjectId, PropostaCreate):
    solicitacao_id: str
    usuario_id: str
    data_envio: datetime
    status: str