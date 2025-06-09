from fastapi import Depends, HTTPException
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt

def role_required(allowed_roles: list[str]):
    def _role_checker(token=Depends(JWTBearer())):
        payload = decode_jwt(token)
        tipo = payload.get("tipo")
        if tipo not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acesso negado para usuários do tipo '{tipo}'."
            )
        return payload  # se quiser usar infos depois
    return _role_checker