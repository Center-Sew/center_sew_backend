# app/services/pagamento_service.py
from app.models.pagamento import Pagamento

class PagamentoService:
    @staticmethod
    async def registrar_pagamento(payload: dict) -> Pagamento:
        pagamento = Pagamento(**payload)
        return await pagamento.insert()

    @staticmethod
    async def obter_status_por_user_e_plano(user_id: str, plano_id: str) -> str:
        pagamento = await Pagamento.find_one({
            "metadata.user_id": user_id,
            "metadata.plano_id": plano_id
        })
        if pagamento:
            return pagamento.status
        return "nao_encontrado"