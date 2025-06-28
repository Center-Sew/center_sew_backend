# app/api/routes/pagamento.py
from fastapi import APIRouter, HTTPException, Query
from app.schemas.pagamento_schema import PagamentoCreate, PagamentoModel
from app.services.pagamento_service import PagamentoService
from typing import Optional

router = APIRouter()

@router.post("/", response_model=PagamentoModel)
async def criar_pagamento(pagamento: PagamentoCreate):
    return await PagamentoService.registrar_pagamento(pagamento.dict())

@router.get("/status")
async def status_pagamento(
    user_id: str = Query(...),
    plano_id: str = Query(...)
):
    status = await PagamentoService.obter_status_por_user_e_plano(user_id, plano_id)
    return {"status": status}