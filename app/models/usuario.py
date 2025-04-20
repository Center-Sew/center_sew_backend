from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Annotated, Literal
from app.models.localizacao import Localizacao


class Usuario(Document):
    nome: str
    email: Annotated[EmailStr, Indexed()]
    senha: str  # Hashed password
    tipo: Literal["empresa", "prestador", "fornecedor"]
    documento: str
    localizacao: Localizacao

    class Settings:
        name = "usuarios"

    class Config:
        json_encoders = {
            EmailStr: lambda v: str(v),
        }
        json_schema_extra = {
            "example": {
                "nome": "Joana da Costura",
                "email": "joana@empresa.com",
                "senha": "hashed_password",
                "tipo": "prestador",
                "documento": "123.456.789-00",
                "localizacao": {
                    "cidade": "Itapetininga",
                    "estado": "SP",
                    "bairro": "Centro",
                    "tipo": "cidade",
                    "valor": "Itapetininga"
                }
            }
        }
