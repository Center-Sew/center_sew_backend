from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId
from app.models.perfil_desejado import PerfilDesejado
from app.schemas.base import BaseModelWithStrObjectId


class SolicitationCreate(BaseModel):
    titulo: str
    descricao: str
    perfil_desejado: PerfilDesejado


class SolicitationModel(BaseModelWithStrObjectId, SolicitationCreate):
    empresa_id: str
    status: str
    data_criacao: str
    interessados: List[str] = []