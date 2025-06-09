from typing import List
import asyncio
from fastapi import APIRouter, Depends, Query
from app.auth.auth_bearer import JWTBearer
from app.schemas.solicitacao_schema import SolicitationCreate, SolicitationModel
from app.services.solicitacao_service import SolicitacaoService
from app.auth.auth_handler import decode_jwt
from app.security.rbac import role_required

router = APIRouter()

@router.get("/", response_model=List[SolicitationModel], dependencies=[Depends(JWTBearer())])
async def listar_solicitacoes(pagina: int = Query(1, ge=1), tamanho: int = Query(10, ge=1, le=100)):
    await asyncio.sleep(3)
    return await SolicitacaoService.listar(pagina, tamanho)

@router.get("/{id}", response_model=SolicitationModel, dependencies=[Depends(JWTBearer())])
async def obter_solicitacao(id: str):
    return await SolicitacaoService.obter_por_id(id)

@router.post("/", response_model=SolicitationModel)
async def criar_solicitacao(
    solicitacao: SolicitationCreate,
    token=Depends(JWTBearer()),
    payload=Depends(role_required(["empresa"]))
):
    payload = decode_jwt(token)
    print("====== teste ======")
    print(payload)
    empresa_id = payload.get("sub")
    return await SolicitacaoService.criar(solicitacao, empresa_id)

@router.put("/{id}", response_model=SolicitationModel)
async def atualizar_solicitacao(
    id: str,
    atualizacao: SolicitationCreate,
    _=Depends(JWTBearer()),
    __=Depends(role_required(["empresa"]))  # Apenas empresa pode atualizar
):
    return await SolicitacaoService.atualizar(id, atualizacao)

@router.delete("/{id}")
async def deletar_solicitacao(
    id: str,
    _=Depends(JWTBearer()),
    __=Depends(role_required(["empresa"]))  # Apenas empresa pode deletar
):
    return await SolicitacaoService.deletar(id)
