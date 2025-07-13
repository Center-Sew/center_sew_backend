# app/models/prestador.py
from beanie import Document, Link
from typing import List, Optional
from app.enums.tipo_fiscal import TipoFiscal
from app.enums.tipo_servico import TipoServico
from app.models.localizacao import Localizacao
from app.models.usuario import Usuario    # NEW – ligação n-para-1

class Prestador(Document):
    usuario:    Link[Usuario]                     # FK para autenticação
    tipo_fiscal: List[TipoFiscal]
    especialidades: List[TipoServico]
    localizacao: Localizacao
    descricao_portfolio: Optional[str] = None
    disponivel: bool = True

    class Settings:
        name = "prestadores"