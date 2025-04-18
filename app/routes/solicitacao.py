from datetime import datetime
from typing import List
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId

from app.auth.auth_bearer import JWTBearer
from app.database.mongo import db
from app.models.solicitacao import SolicitationCreate, SolicitationModel
from utils.mongo_helpers import serialize_doc

router = APIRouter()

# 🔍 GET com paginação
@router.get("/", response_model=List[SolicitationModel], dependencies=[Depends(JWTBearer())])
async def detalhes_solicitacao(
    pagina: int = Query(1, ge=1),
    tamanho: int = Query(10, ge=1, le=100)
):
    await asyncio.sleep(3)
    skip = (pagina - 1) * tamanho
    cursor = db.solicitacoes.find().skip(skip).limit(tamanho)
    return [SolicitationModel(**serialize_doc(doc)) for doc in cursor]

# 🔍 GET por ID
@router.get("/{id}", response_model=SolicitationModel, dependencies=[Depends(JWTBearer())])
async def obter_solicitacao(id: str):
    try:
        solicitacao = db.solicitacoes.find_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    return SolicitationModel(**serialize_doc(solicitacao))

# 📝 POST - Criar nova
@router.post("/", response_model=SolicitationModel, dependencies=[Depends(JWTBearer())])
async def criar_solicitacao(solicitacao: SolicitationCreate, usuario=Depends(JWTBearer())):
    doc = solicitacao.dict()
    doc["empresa_id"] = usuario["_id"]  # Assumindo que o JWTBearer retorna o usuário autenticado
    doc["data_criacao"] = datetime.utcnow().isoformat()
    doc["status"] = "aberta"
    doc["interessados"] = []

    result = db.solicitacoes.insert_one(doc)
    nova = db.solicitacoes.find_one({"_id": result.inserted_id})
    return SolicitationModel(**serialize_doc(nova))

# ✏️ PUT - Atualizar por ID
@router.put("/{id}", response_model=SolicitationModel, dependencies=[Depends(JWTBearer())])
async def atualizar_solicitacao(id: str, atualizacao: SolicitationCreate):
    try:
        result = db.solicitacoes.update_one(
            {"_id": ObjectId(id)},
            {"$set": atualizacao.dict()}
        )
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    atualizada = db.solicitacoes.find_one({"_id": ObjectId(id)})
    return SolicitationModel(**serialize_doc(atualizada))

# ❌ DELETE - Remover por ID
@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deletar_solicitacao(id: str):
    try:
        result = db.solicitacoes.delete_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    return {"mensagem": "Solicitação removida com sucesso."}
