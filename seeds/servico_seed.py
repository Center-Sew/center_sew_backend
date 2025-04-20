from pathlib import Path
import json
from app.models.servico import Servico

async def seed_servicos():
    await Servico.find_all().delete()
    path = Path(__file__).parent / "data" / "servicos.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        servico = Servico(**item)
        await servico.insert()

    print("✅ Seed de serviços carregado a partir de JSON.")