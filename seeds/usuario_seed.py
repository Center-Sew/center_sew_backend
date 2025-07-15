# seeds/usuario_seed.py
import json
from pathlib import Path
from app.models.usuario import Usuario
from app.models.localizacao import Localizacao
from app.auth.auth_handler import hash_password

async def seed_usuarios():
    await Usuario.find_all().delete()

    path = Path(__file__).parent / "data" / "usuarios.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        usuario = Usuario(
            nome=entry["nome"],
            email=entry["email"],
            senha=hash_password(entry["senha"]),
            tipo=entry["tipo"],
            documento=entry["documento"],
            localizacao=Localizacao(**entry["localizacao"])
        )
        await usuario.insert()

    print("✅ Seed de usuários carregado a partir de arquivo.")