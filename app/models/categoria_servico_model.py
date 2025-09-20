# app/models/categoria_servico.py

from beanie import Document
from pydantic import BaseModel
from typing import List

class CategoriaServico(Document):
    nome: str  # Ex: "Costura Blusa"
    tipo: str  # Ex: "costura", "estamparia", etc.
    subcategorias: List[str]

    class Settings:
        name = "categorias_servico"