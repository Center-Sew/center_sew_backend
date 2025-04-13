from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decode_jwt

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            if decode_jwt(token):
                return credentials.credentials
            raise HTTPException(status_code=403, detail="Token inválido")
        raise HTTPException(status_code=403, detail="Token não encontrado")