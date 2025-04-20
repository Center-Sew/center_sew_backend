from typing import List
from fastapi import HTTPException

from app.models.prestador import Prestador
from app.schemas.prestador_schema import PrestadorCreate, PrestadorResponse

class PrestadorService:
    @staticmethod
    async def criar(data: PrestadorCreate) -> PrestadorResponse:
        prestador = Prestador(**data.dict())
        await prestador.insert()
        return PrestadorResponse(**prestador.dict(by_alias=True))

    @staticmethod
    async def listar() -> List[PrestadorResponse]:
        docs = await Prestador.find_all().to_list()
        return [PrestadorResponse(**doc.dict(by_alias=True)) for doc in docs]

    @staticmethod
    async def obter_por_id(prestador_id: str) -> PrestadorResponse:
        doc = await Prestador.get(prestador_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Prestador não encontrado")
        return PrestadorResponse(**doc.dict(by_alias=True))

    @staticmethod
    async def atualizar(prestador_id: str, dados: PrestadorCreate) -> PrestadorResponse:
        prestador = await Prestador.get(prestador_id)
        if not prestador:
            raise HTTPException(status_code=404, detail="Prestador não encontrado")
        await prestador.set(dados.dict())
        return PrestadorResponse(**prestador.dict(by_alias=True))

    @staticmethod
    async def deletar(prestador_id: str):
        prestador = await Prestador.get(prestador_id)
        if not prestador:
            raise HTTPException(status_code=404, detail="Prestador não encontrado")
        await prestador.delete()
        return {"mensagem": "Prestador removido com sucesso."}
