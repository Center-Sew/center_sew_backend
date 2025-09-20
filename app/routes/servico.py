# app/routes/servicos_routes.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any

from app.schemas.servico_schema import ServicoCreate, ServicoResponse
from app.services.servico_service import ServicoService
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt

router = APIRouter()

def _json_ok(payload: Dict[str, Any], status_code: int = 200):
    return JSONResponse(content=payload, status_code=status_code, media_type="application/json; charset=utf-8")

# 🔴 NOVO: helper para ler o user id do payload
def _get_user_id(payload: dict) -> str:
    """
    Extrai o id do usuário do payload do JWT, tolerando diferentes chaves.
    Prioridade: user_id > sub > uid
    """
    uid = payload.get("user_id") or payload.get("sub") or payload.get("uid")
    if not uid:
        return ""
    return str(uid)

@router.post("/", response_model=ServicoResponse)
async def criar_servico(dados: ServicoCreate, token=Depends(JWTBearer())):
    payload = decode_jwt(token)
    empresa_id = _get_user_id(payload)          # ⬅️ antes estava payload.get("user_id")
    # se sua assinatura do service aceitar empresa_id, passe; se não, ignore.
    return await ServicoService.criar(dados)     # ou: await ServicoService.criar(dados, empresa_id)

@router.get("/", response_model=list[ServicoResponse], dependencies=[Depends(JWTBearer())])
async def listar_servicos():
    return await ServicoService.listar()

@router.get("/{id}", response_model=ServicoResponse, dependencies=[Depends(JWTBearer())])
async def obter_servico(id: str):
    return await ServicoService.obter_por_id(id)

# ========= NOVAS ROTAS (ajustadas) =========

@router.patch("/{id}/status", dependencies=[Depends(JWTBearer())])
async def atualizar_status_servico(id: str, body: Dict[str, Any], token=Depends(JWTBearer())):
    payload = decode_jwt(token)
    solicitante_id = _get_user_id(payload)       # ⬅️ ajuste aqui
    novo_status = (body.get("status") or "").strip()
    result = await ServicoService.atualizar_status(id, novo_status, solicitante_id)
    return _json_ok(result)

@router.put("/{id}/finalizar", dependencies=[Depends(JWTBearer())])
async def finalizar_servico(id: str, token=Depends(JWTBearer())):
    payload = decode_jwt(token)
    solicitante_id = _get_user_id(payload)       # ⬅️ ajuste aqui
    # Debug opcional:
    # print("[finalizar] solicitante_id=", solicitante_id)
    result = await ServicoService.finalizar(id, solicitante_id)
    return _json_ok(result)