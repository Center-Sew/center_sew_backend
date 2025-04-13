from fastapi import APIRouter, Depends
from app.models.service import ServiceRequest
from app.auth.auth_bearer import JWTBearer
from app.database.mongo import db

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())])
def criar_servico(service: ServiceRequest):
    db.services.insert_one(service.dict())
    return {"msg": "Serviço criado com sucesso"}

@router.get("/", dependencies=[Depends(JWTBearer())])
def listar_servicos():
    return list(db.services.find({}, {"_id": 0}))

@router.get("/{titulo}", dependencies=[Depends(JWTBearer())])
def buscar_por_titulo(titulo: str):
    return db.services.find_one({"titulo": titulo}, {"_id": 0})