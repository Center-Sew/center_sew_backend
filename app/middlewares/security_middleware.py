from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("uvicorn.error")


class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int = 1 * 1024 * 1024):  # padrão: 1MB
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        # 🔐 Limita tamanho do corpo
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.body()
            if len(body) > self.max_body_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"Payload muito grande. Limite: {self.max_body_size // 1024} KB"
                )

        # 📘 Log de requisição
        logger.info(f"{request.method} {request.url.path} from {request.client.host}")

        return await call_next(request)