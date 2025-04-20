from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from app.models.localizacao import Localizacao
from app.schemas.base import BaseModelWithStrObjectId  # <-- Base importada

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo: Literal["empresa", "prestador", "fornecedor"]
    documento: str
    localizacao: Localizacao

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(BaseModelWithStrObjectId, UsuarioBase):  # <-- Herdando da base com tratamento de ObjectId
    pass

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
