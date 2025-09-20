# app/services/categoria_servico_service.py

from typing import List
from app.models.categoria_servico_model import CategoriaServico
from app.schemas.categoria_servico_schema import CategoriaServicoSchema

class CategoriaServicoService:
    @staticmethod
    async def listar() -> List[CategoriaServicoSchema]:
        docs = await CategoriaServico.find_all().to_list()
        return [CategoriaServicoSchema(**d.dict()) for d in docs]