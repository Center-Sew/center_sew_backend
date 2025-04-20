from typing import Optional

from pydantic import BaseModel
from app.enums.tipo_localizacao_alvo import TipoLocalizacaoAlvo

class Localizacao(BaseModel):
    cidade: Optional[str]
    estado: Optional[str]
    bairro: Optional[str]
    tipo: Optional[TipoLocalizacaoAlvo]
    valor: Optional[str]
