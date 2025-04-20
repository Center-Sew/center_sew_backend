from typing import List
from fastapi import HTTPException
from app.models.servico import Servico
from app.schemas.servico_schema import ServicoCreate, ServicoResponse
from beanie.operators import In

class ServicoService:
    @staticmethod
    async def criar(dados: ServicoCreate, empresa_id: str) -> ServicoResponse:
        novo_servico = Servico(
            **dados.dict(),
            empresa_id=empresa_id,
            status="em_andamento"
        )
        await novo_servico.insert()
        return ServicoResponse(**novo_servico.dict(by_alias=True))

    @staticmethod
    async def listar() -> List[ServicoResponse]:
        servicos = await Servico.find_all().to_list()
        return [ServicoResponse(**s.dict(by_alias=True)) for s in servicos]

    @staticmethod
    async def obter_por_id(servico_id: str) -> ServicoResponse:
        servico = await Servico.get(servico_id)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        return ServicoResponse(**servico.dict(by_alias=True))