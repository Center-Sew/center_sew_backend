from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt
from fastapi import Request

router = APIRouter()

@router.get("/me", dependencies=[Depends(JWTBearer())])
def meu_perfil(request: Request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = decode_jwt(token)
    user = db.users.find_one({"email": payload["user_id"]}, {"_id": 0, "password": 0})
    return user