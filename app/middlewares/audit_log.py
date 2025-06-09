from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn.access")

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logger.info(
            "%s %s - %s - IP: %s",
            request.method,
            request.url.path,
            response.status_code,
            request.client.host,
        )
        return response