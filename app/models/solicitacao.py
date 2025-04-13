from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class SolicitationModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    titulo: str
    subtitulo: str
    descricao: str
    interessados: int

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
