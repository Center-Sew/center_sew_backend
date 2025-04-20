from typing import List
from fastapi import HTTPException
from app.models.solicitacao import Solicitacao
from app.schemas.solicitacao_schema import SolicitationCreate, SolicitationModel

class SolicitacaoService:
    @staticmethod
    async def listar(pagina: int = 1, tamanho: int = 10) -> List[SolicitationModel]:
        skip = (pagina - 1) * tamanho
        documentos = await Solicitacao.find_all().skip(skip).limit(tamanho).to_list()
        return [SolicitationModel(**doc.dict(by_alias=True)) for doc in documentos]

    @staticmethod
    async def obter_por_id(solicitacao_id: str) -> SolicitationModel:
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        return SolicitationModel(**doc.dict(by_alias=True))

    @staticmethod
    async def criar(dados: SolicitationCreate, empresa_id: str) -> SolicitationModel:
        nova = Solicitacao(
            **dados.dict(),
            empresa_id=empresa_id,
            status="aberta",
            interessados=[]
        )
        await nova.insert()
        return SolicitationModel(**nova.dict(by_alias=True))

    @staticmethod
    async def atualizar(solicitacao_id: str, atualizacao: SolicitationCreate) -> SolicitationModel:
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        await doc.set(atualizacao.dict())
        return SolicitationModel(**doc.dict(by_alias=True))

    @staticmethod
    async def deletar(solicitacao_id: str):
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        await doc.delete()
        return {"mensagem": "Solicitação removida com sucesso."}