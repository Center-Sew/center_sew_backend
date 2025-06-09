from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

def custom_rate_limit_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Limite de tentativas excedido. Tente novamente em instantes."}
    )