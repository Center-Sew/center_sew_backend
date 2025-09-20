# app/routes/proposta.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from app.schemas.proposta_schema import PropostaCreate, PropostaModel
from app.security.rbac import role_required
from app.services.proposta_service import PropostaService

router = APIRouter(prefix="/solicitacoes/{id}/propostas", tags=["Propostas"])

# Criar proposta (usuário do tipo prestador)
@router.post("/", response_model=PropostaModel, status_code=201)
async def enviar_proposta(
    body: PropostaCreate,
    id: str = Path(..., description="ID da solicitação"),
    token = Depends(role_required(["prestador"])),
):
    usuario_id = token["sub"]
    return await PropostaService.criar(id, usuario_id, body)


# Listar propostas (usuário dono da solicitação ou interessado)
@router.get("/", response_model=list[PropostaModel])
async def listar_propostas(
    id: str,
    token = Depends(role_required(["empresa", "prestador"]))
):
    usuario_id = token.get("sub")
    return await PropostaService.listar_por_solicitacao(id, usuario_id)


# Listar apenas a proposta do usuário logado para essa solicitação
@router.get("/minha", response_model=List[PropostaModel])
async def get_minha_proposta(
    id: str = Path(..., description="ID da solicitação"),
    token = Depends(role_required(["prestador"]))
):
    prestador_id = token.get("sub")
    # ✅ chama o método novo
    return await PropostaService.buscar_propostas_do_prestador(id, prestador_id)


# Aceitar proposta (usuário que criou a solicitação)
@router.post("/{proposta_id}/aceitar")
async def aceitar_proposta(
    id: str = Path(..., description="ID da solicitação"),
    proposta_id: str = Path(..., description="ID da proposta"),
    token = Depends(role_required(["empresa"])),  # ou qualquer tipo que possa aceitar
):
    usuario_id = token.get("sub")
    return await PropostaService.aceitar_proposta(id, proposta_id, usuario_id)


@router.post("/{proposta_id}/rejeitar")
async def rejeitar_proposta(
    id: str = Path(..., description="ID da solicitação"),
    proposta_id: str = Path(..., description="ID da proposta"),
    token = Depends(role_required(["empresa"]))
):
    return await PropostaService.rejeitar_proposta(
        solicitacao_id=id,
        proposta_id=proposta_id,
        usuario_id=token["sub"]
    )