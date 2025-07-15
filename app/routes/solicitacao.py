import json
from fastapi import APIRouter, Depends, Query, Form, File, UploadFile
from typing import List
from app.models.perfil_desejado import PerfilDesejado
from app.schemas.solicitacao_schema import SolicitationModel, SolicitationCreate
from app.security.rbac import role_required
from app.services.solicitacao_service import SolicitacaoService
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt

router = APIRouter()


# 📥 LISTAR (empresa só vê suas, prestador vê todas abertas)
@router.get("/", response_model=List[SolicitationModel])
async def listar_solicitacoes(
    token_payload: dict = Depends(role_required(["empresa", "prestador"])),
    pagina: int = Query(1, ge=1),
    tamanho: int = Query(10, ge=1, le=100)
):
    return await SolicitacaoService.listar(token_payload, pagina, tamanho)


# 🔍 OBTER POR ID (ambos podem ver)
@router.get("/{id}", response_model=SolicitationModel)
async def obter_solicitacao(
    id: str,
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    return await SolicitacaoService.obter_por_id(id)


@router.post("/", response_model=SolicitationModel)
async def criar_solicitacao(
    payload: str = Form(...),
    imagens: List[UploadFile] = File(default=[]),
    token_payload: dict = Depends(role_required(["empresa"]))
):
    """
    Cria uma nova solicitação.

    Corpo da requisição:
    - payload (str): JSON serializado compatível com o modelo `SolicitationCreate`
    - imagens (List[UploadFile], opcional): fotos da solicitação

    Requer autenticação de empresa (token JWT com tipo=empresa).
    """
    try:
        dados_dict = json.loads(payload)
        dados = SolicitationCreate(**dados_dict)
    except Exception as e:
        raise ValueError(f"Erro ao decodificar JSON de payload: {e}")

    empresa_id = token_payload.get("sub")
    return await SolicitacaoService.criar(dados, empresa_id, imagens)


# ✏️ ATUALIZAR (apenas empresa)
@router.put("/{id}", response_model=SolicitationModel)
async def atualizar_solicitacao(
    id: str,
    atualizacao: SolicitationCreate,
    token_payload: dict = Depends(role_required(["empresa"]))
):
    return await SolicitacaoService.atualizar(id, atualizacao)


# ❌ DELETAR (apenas empresa)
@router.delete("/{id}")
async def deletar_solicitacao(
    id: str,
    token_payload: dict = Depends(role_required(["empresa"]))
):
    return await SolicitacaoService.deletar(id)