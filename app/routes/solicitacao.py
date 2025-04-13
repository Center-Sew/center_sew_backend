from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.database.mongo import db

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer())])
def detalhes_solicitacao():
    return list(db.solicitacoes.find({}, {"_id": 0}))