from typing import Literal, Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.enums.tipo_fiscal import TipoFiscal
from app.enums.tipo_servico import TipoServico
from app.models.localizacao import Localizacao
from app.schemas.base import BaseModelWithStrObjectId

# Campos básicos
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo: Literal["empresa", "prestador", "fornecedor"]
    documento: str
    telefone: Optional[str] = None
    celular:  Optional[str] = None
    localizacao: Localizacao
    foto: Optional[str] = Field(default=None, alias="foto_url")

# Registro de novo usuário
class UsuarioCreate(UsuarioBase):
    senha: str

    # Campos adicionais para prestador
    tipo_fiscal: Optional[List[TipoFiscal]] = None
    especialidades: Optional[List[TipoServico]] = None
    descricao_portfolio: Optional[str] = None

    # Campos adicionais para empresa
    razaosocial: Optional[str] = None
    segmento: Optional[str] = None

# Resposta simples com ID
class UsuarioResponse(BaseModelWithStrObjectId, UsuarioBase):
    pass

# Login
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

# Payload do usuário autenticado
class UsuarioPayload(BaseModelWithStrObjectId, UsuarioBase):
    pass

# Resposta de autenticação
class UsuarioAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800
    user: UsuarioPayload