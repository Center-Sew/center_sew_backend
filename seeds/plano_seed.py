import json
from pathlib import Path
from app.models.plano import Plano

async def seed_planos():
    await Plano.find_all().delete()

    path = Path(__file__).parent / "data" / "planos.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        plano = Plano(**item)
        await plano.insert()

    print(f"✅ Seed de planos gerada com {len(data)} registros.")