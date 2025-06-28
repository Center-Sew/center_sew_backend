from pydantic import BaseModel, EmailStr
from typing import Literal
from app.models.localizacao import Localizacao
from app.schemas.base import BaseModelWithStrObjectId


# 🧱 Campos básicos reutilizáveis em várias operações
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo: Literal["empresa", "prestador", "fornecedor"]
    documento: str
    localizacao: Localizacao


# 🛠️ Usado no /register
class UsuarioCreate(UsuarioBase):
    senha: str


# 🧾 Usado no /register (resposta com _id)
class UsuarioResponse(BaseModelWithStrObjectId, UsuarioBase):
    pass


# 🔐 Usado no /login
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


# 🧍 Usado para retornar o usuário autenticado no /login
class UsuarioPayload(BaseModelWithStrObjectId, UsuarioBase):
    pass


# 🎁 Resposta completa de autenticação
class UsuarioAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800
    user: UsuarioPayload