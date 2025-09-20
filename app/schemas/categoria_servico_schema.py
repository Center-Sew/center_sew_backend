# app/schemas/categoria_servico_schema.py

from pydantic import BaseModel
from typing import List

class CategoriaServicoSchema(BaseModel):
    nome: str
    tipo: str
    subcategorias: List[str]