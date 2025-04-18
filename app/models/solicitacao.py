from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Union
from bson import ObjectId


class LocalizacaoAlvo(BaseModel):
    tipo: Literal["raio", "cidade", "estado"]
    valor: str  # Ex: "10km", "São Paulo", "SP"


class PerfilDesejado(BaseModel):
    tipo_fiscal: List[Literal["CPF", "CNPJ"]]
    tipo_servico: str
    descricao: str
    localizacao_alvo: Optional[LocalizacaoAlvo]


class SolicitationCreate(BaseModel):
    titulo: str
    descricao: str
    perfil_desejado: PerfilDesejado

class SolicitationModel(SolicitationCreate):
    id: Optional[str] = Field(alias="_id")
    empresa_id: str
    data_criacao: Optional[str]  # pode ser datetime no futuro
    status: str = "aberta"
    interessados: Optional[List[dict]] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
