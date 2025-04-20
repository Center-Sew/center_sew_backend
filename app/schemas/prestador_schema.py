from pydantic import BaseModel, Field
from typing import List, Optional

from app.enums.tipo_fiscal import TipoFiscal
from app.enums.tipo_localizacao_alvo import TipoLocalizacaoAlvo
from app.enums.tipo_servico import TipoServico

class LocalizacaoSchema(BaseModel):
    cidade: Optional[str] = None
    estado: Optional[str] = None
    bairro: Optional[str] = None
    tipo: Optional[TipoLocalizacaoAlvo] = None
    valor: Optional[str] = None

class PrestadorCreate(BaseModel):
    nome: str
    tipo_fiscal: List[TipoFiscal]
    especialidades: List[TipoServico]
    localizacao: LocalizacaoSchema
    descricao_portfolio: Optional[str] = None
    disponivel: bool = True

class PrestadorResponse(PrestadorCreate):
    id: str = Field(alias="_id")

    class Config:
        validate_by_name = True
        from_attributes = True
