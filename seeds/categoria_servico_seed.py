# seeds/categoria_servico_seed.py

from pathlib import Path
import json
from app.models.categoria_servico_model import CategoriaServico

async def seed_categorias_servico():
    await CategoriaServico.find_all().delete()

    path = Path(__file__).parent / "data" / "categorias_servico.json"
    with open(path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for item in dados:
        await CategoriaServico(**item).insert()

    print("✅ Seed de categorias de serviço carregada do JSON.")