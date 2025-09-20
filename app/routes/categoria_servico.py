# app/routes/categoria_servico.py

from fastapi import APIRouter
from typing import List
from app.services.categoria_servico_service import CategoriaServicoService
from app.schemas.categoria_servico_schema import CategoriaServicoSchema

router = APIRouter()

@router.get("/", response_model=List[CategoriaServicoSchema])
async def listar_categorias_servico():
    return await CategoriaServicoService.listar()