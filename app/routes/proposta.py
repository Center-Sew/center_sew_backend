# app/routes/proposta.py
from fastapi import APIRouter, Depends, Path
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
    return await PropostaService.listar_por_solicitacao(id)


# Aceitar proposta (usuário que criou a solicitação)
@router.post("/{proposta_id}/aceitar")
async def aceitar_proposta(
    id: str = Path(..., description="ID da solicitação"),
    proposta_id: str = Path(..., description="ID da proposta"),
    token = Depends(role_required(["empresa"])),  # ou qualquer tipo que possa aceitar
):
    usuario_id = token.get("sub")
    return await PropostaService.aceitar_proposta(id, proposta_id, usuario_id)