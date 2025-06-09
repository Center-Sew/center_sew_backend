from typing import List
from beanie import PydanticObjectId
from app.models.plano import Plano

class PlanoService:

    @staticmethod
    async def listar(pagina: int, tamanho: int) -> List[Plano]:
        skip = (pagina - 1) * tamanho
        return await Plano.find_all().skip(skip).limit(tamanho).to_list()

    @staticmethod
    async def obter_por_id(id: str) -> Plano:
        return await Plano.get(PydanticObjectId(id))