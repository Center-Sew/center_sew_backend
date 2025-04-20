from fastapi import APIRouter, Depends
from typing import List
from app.schemas.servico_schema import ServicoCreate, ServicoResponse
from app.services.servico_service import ServicoService
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt

router = APIRouter()

@router.post("/", response_model=ServicoResponse)
async def criar_servico(dados: ServicoCreate, token=Depends(JWTBearer())):
    payload = decode_jwt(token)
    empresa_id = payload.get("user_id")
    return await ServicoService.criar(dados, empresa_id)

@router.get("/", response_model=List[ServicoResponse], dependencies=[Depends(JWTBearer())])
async def listar_servicos():
    return await ServicoService.listar()

@router.get("/{id}", response_model=ServicoResponse, dependencies=[Depends(JWTBearer())])
async def obter_servico(id: str):
    return await ServicoService.obter_por_id(id)