from pydantic import BaseModel

class PrestadorDetalhe(BaseModel):
    nome: str
    especialidade: str
    localizacao: str