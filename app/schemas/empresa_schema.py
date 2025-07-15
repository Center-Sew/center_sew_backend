# app/schemas/empresa_schema.py
from pydantic import BaseModel
from typing import Optional

class EmpresaSlim(BaseModel):
    id: str
    razao_social: str           # ✅ Adicionado
    nome_fantasia: str          # ✅ Adicionado
    cnpj: str
    cidade: str
    estado: str
    bairro: str