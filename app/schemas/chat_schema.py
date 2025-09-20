from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Annotated, Optional
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]

class MensagemCreate(BaseModel):
    proposta_id: Optional[str] = None
    servico_id: Optional[str] = None
    destinatario_id: str
    texto: str

    # Validação extra (opcional) para garantir que um dos dois esteja presente
    def validate_ids(self):
        if not self.proposta_id and not self.servico_id:
            raise ValueError("Um dos campos 'proposta_id' ou 'servico_id' é obrigatório.")

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_ids()

class MensagemResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    proposta_id: Optional[PyObjectId] = None
    servico_id: Optional[PyObjectId] = None
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