from typing import List, Literal, Optional
from pydantic import BaseModel

from app.enums.tipo_fiscal import TipoFiscal
from app.models.localizacao import Localizacao


class PerfilDesejado(BaseModel):
    tipo_fiscal: List[TipoFiscal]
    tipo_servico: str
    descricao: str
    localizacao_alvo: Optional[Localizacao]