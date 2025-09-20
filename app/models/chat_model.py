from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class MensagemChat(Document):
    proposta_id: Optional[ObjectId] = None
    servico_id: Optional[ObjectId] = None
    remetente_id: ObjectId
    destinatario_id: ObjectId
    texto: str
    lido: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_mensagens"

    model_config = {
        "json_encoders": {ObjectId: str},
        "arbitrary_types_allowed": True,
    }