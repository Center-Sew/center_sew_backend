from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from app.models.perfil_desejado import PerfilDesejado
from app.schemas.base import BaseModelWithStrObjectId


class SolicitationCreate(BaseModel):
    titulo: str
    descricao: str
    perfil_desejado: PerfilDesejado


class UsuarioSlim(BaseModel):
    id: str
    nome: str
    email: str
    segmento: Optional[str] = None
    localizacao: Optional[dict] = None


class SolicitationModel(BaseModelWithStrObjectId, SolicitationCreate):
    usuario_id: str
    usuario: Optional[UsuarioSlim] = None  # opcional na resposta
    status: str
    data_criacao: datetime
    interessados: int = 0
    imagens: Optional[List[str]] = []