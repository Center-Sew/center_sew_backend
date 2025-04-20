from beanie import Document
from typing import List, Optional
from app.enums.tipo_fiscal import TipoFiscal
from app.enums.tipo_servico import TipoServico
from app.models.localizacao import Localizacao

class Prestador(Document):
    nome: str
    tipo_fiscal: List[TipoFiscal]
    especialidades: List[TipoServico]
    localizacao: Localizacao
    descricao_portfolio: Optional[str] = None
    disponivel: bool = True

    class Settings:
        name = "prestadores"