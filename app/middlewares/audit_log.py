from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn.access")


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500  # ou outro valor que represente falha
            logger.exception("Erro durante a requisição: %s", e)
            raise

        method = request.method
        path = request.url.path
        ip = request.client.host if request.client else "unknown"

        logger.info(f"{method} {path} - {status_code} - IP: {ip}")
        return response