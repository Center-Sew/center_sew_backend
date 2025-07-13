# app/models/empresa.py
from beanie import Document, Link
from typing import Optional
from app.models.usuario import Usuario
from app.models.localizacao import Localizacao

class Empresa(Document):
    usuario:        Link[Usuario]            # FK para autenticação
    razaosocial:    str
    cnpj:           str
    segmento:       Optional[str] = None
    localizacao:    Localizacao

    class Settings:
        name = "empresas"