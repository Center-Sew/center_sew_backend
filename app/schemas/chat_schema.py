from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]

class MensagemCreate(BaseModel):
    proposta_id: str
    destinatario_id: str
    texto: str

class MensagemResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    proposta_id: PyObjectId
    remetente_id: PyObjectId
    destinatario_id: PyObjectId
    texto: str
    lido: bool
    timestamp: datetime

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
    }