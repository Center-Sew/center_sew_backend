from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.utils.rate_limit_handler import custom_rate_limit_handler
from slowapi.middleware import SlowAPIMiddleware
from app.extensions.limiter_extension import limiter

from app.middlewares.security_middleware import SecurityMiddleware
from app.middlewares.audit_log import AuditLogMiddleware
from app.routes import auth, profile, prestador, servico, solicitacao, plano
from app.database.mongo import init_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo()
    yield

app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(SecurityMiddleware, max_body_size=1 * 1024 * 1024)

# CORS - Configure logo após instanciar o app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # substitua pelo domínio real do frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],    
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(servico.router, prefix="/services", tags=["services"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(prestador.router, prefix="/prestador", tags=["prestador"])
app.include_router(solicitacao.router, prefix="/solicitacoes", tags=["solicitacoes"])
app.include_router(plano.router, prefix="/planos", tags=["planos"])

@app.get("/")
def home():
    return {"msg": "API Center Sew, conexão entre empresas e costureiras"}