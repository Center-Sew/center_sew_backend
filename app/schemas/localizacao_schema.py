from typing import Optional
from pydantic import BaseModel
from app.enums.tipo_localizacao_alvo import TipoLocalizacaoAlvo

class LocalizacaoSchema(BaseModel):
    cidade: Optional[str] = None
    estado: Optional[str] = None
    bairro: Optional[str] = None
    tipo: Optional[TipoLocalizacaoAlvo] = None
    valor: Optional[str] = None
