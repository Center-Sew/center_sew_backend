from fastapi import APIRouter, Request, HTTPException, Query
from app.schemas.mercado_pago import PagamentoDetalhesSchema
from app.services.mercado_pago_service import buscar_detalhes_pagamento
from app.repositories.pagamento_repository import salvar_pagamento
import logging
import json

router = APIRouter()

@router.post("/webhook/mercado-pago")
async def webhook_mercado_pago(
    id: str = Query(...),
    topic: str = Query(...)
):
    try:
        logging.info(f"📥 Webhook recebido: topic={topic}, id={id}")

        if topic != "payment":
            return {"status": "ignored"}

        detalhes_dict = await buscar_detalhes_pagamento(id)

        # Valida e tipa usando o schema Pydantic
        detalhes = PagamentoDetalhesSchema.model_validate(detalhes_dict)

        logging.info(f"📦 Pagamento recebido - status: {detalhes.status}")
        print(json.dumps(detalhes_dict, indent=2, ensure_ascii=False))

        await salvar_pagamento({
            "payment_id": detalhes.id,
            "user_id": detalhes.metadata.user_id,
            "plano_id": detalhes.metadata.plano_id,
            "descricao": detalhes.metadata.plano_nome,
            "valor": detalhes.metadata.plano_valor,
            "tipo_usuario": detalhes.metadata.tipo_usuario,
            "status": detalhes.status,
            "status_detail": detalhes.status_detail,
            "raw_payload": detalhes_dict
        })

        return {"status": "ok"}

    except Exception as e:
        logging.error(f"❌ Erro no webhook Mercado Pago: {e}")
        raise HTTPException(status_code=400, detail="Erro no processamento do webhook")