from beanie import Document, Indexed
from pydantic import EmailStr, Field
from typing import Annotated, Literal, Optional, List
from bson import ObjectId
from app.models.localizacao import Localizacao
from app.enums.tipo_fiscal import TipoFiscal
from app.enums.tipo_servico import TipoServico

class Usuario(Document):
    nome: str
    email: Annotated[EmailStr, Indexed()]
    senha: str
    tipo: Literal["empresa", "prestador", "fornecedor"]
    documento: str
    telefone: Optional[str] = None
    celular: Optional[str] = None
    localizacao: Localizacao
    foto:   Optional[str] = None

    # Campos de empresa
    razaosocial: Optional[str] = None
    segmento: Optional[str] = None

    # Campos de prestador
    tipo_fiscal: Optional[List[TipoFiscal]] = None
    especialidades: Optional[List[TipoServico]] = None
    descricao_portfolio: Optional[str] = None
    disponivel: Optional[bool] = True

    class Settings:
        name = "usuarios"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            EmailStr: str,
            ObjectId: str
        },
        "json_schema_extra": {
            "example": {
                "nome": "Joana da Costura",
                "email": "joana@empresa.com",
                "senha": "hashed_password",
                "tipo": "prestador",
                "documento": "123.456.789-00",
                "telefone": "(11) 1234-5678",
                "celular": "(11) 99999-8888",
                "localizacao": {
                    "cidade": "Itapetininga",
                    "estado": "SP",
                    "bairro": "Centro",
                    "tipo": "cidade",
                    "valor": "Itapetininga"
                },
                "tipo_fiscal": ["CPF"],
                "especialidades": ["Ajuste de uniforme"],
                "descricao_portfolio": "Faço ajustes sob medida.",
                "disponivel": True
            }
        }
    }
