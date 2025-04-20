from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer

router = APIRouter()

@router.get("/{nome}", dependencies=[Depends(JWTBearer())])
def detalhes_prestador(nome: str):
    return db.prestadores.find_one({"nome": nome}, {"_id": 0})