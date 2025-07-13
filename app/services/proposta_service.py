import asyncio
from typing import List
from fastapi import HTTPException
from app.models.proposta import Proposta
from app.models.solicitacao import Solicitacao
from app.schemas.proposta_schema import PropostaCreate, PropostaModel

class PropostaService:

    @staticmethod
    async def criar(solicitacao_id: str, prestador_id: str, dados: PropostaCreate) -> PropostaModel:
        proposta = Proposta(
            solicitacao_id=solicitacao_id,
            prestador_id=prestador_id,
            mensagem=dados.mensagem,
        )
        await proposta.insert()
        return PropostaModel(**proposta.dict(by_alias=True))

    @staticmethod
    async def listar_por_solicitacao(solicitacao_id: str) -> List[PropostaModel]:
        docs = await Proposta.find({"solicitacao_id": solicitacao_id}).sort("-data_envio").to_list()
        return [PropostaModel(**d.dict(by_alias=True)) for d in docs]
    
    @staticmethod
    async def aceitar_proposta(solicitacao_id: str, proposta_id: str, empresa_id: str):
        # ✅ Verifica se a solicitação pertence à empresa
        solicitacao = await Solicitacao.get(solicitacao_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        if solicitacao.empresa_id != empresa_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        # ✅ Busca todas as propostas
        propostas = await Proposta.find({"solicitacao_id": solicitacao_id}).to_list()

        if not any(p.id == proposta_id for p in propostas):
            raise HTTPException(status_code=404, detail="Proposta não encontrada")

        updates = []
        for p in propostas:
            novo_status = "aceita" if str(p.id) == proposta_id else "recusada"
            if p.status != novo_status:
                p.status = novo_status
                updates.append(p.save_changes())

        await asyncio.gather(*updates)
        return {"mensagem": "Proposta aceita com sucesso!"}
    
    @staticmethod
    async def contar_interessados_unicos(solicitacao_id: str) -> int:
        propostas = await Proposta.find(Proposta.solicitacao_id == solicitacao_id).to_list()
        prestadores_ids = {p.prestador_id for p in propostas}
        return len(prestadores_ids)