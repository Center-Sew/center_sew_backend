from typing import List
import asyncio
from fastapi import APIRouter, Depends, Query
from app.auth.auth_bearer import JWTBearer
from app.schemas.plano_schema import PlanoModel
from app.services.plano_service import PlanoService

router = APIRouter()

@router.get("/", response_model=List[PlanoModel], dependencies=[Depends(JWTBearer())])
async def listar_planos(pagina: int = Query(1, ge=1), tamanho: int = Query(10, ge=1, le=100)):
    await asyncio.sleep(1)
    return await PlanoService.listar(pagina, tamanho)

@router.get("/{id}", response_model=PlanoModel, dependencies=[Depends(JWTBearer())])
async def obter_plano(id: str):
    return await PlanoService.obter_por_id(id)