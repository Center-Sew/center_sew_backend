from contextlib import asynccontextmanager
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.utils.rate_limit_handler import custom_rate_limit_handler
from slowapi.middleware import SlowAPIMiddleware
from app.extensions.limiter_extension import limiter

from app.middlewares.security_middleware import SecurityMiddleware
from app.middlewares.audit_log import AuditLogMiddleware
from app.routes import (
    auth, imagem_routes, profile, prestador, proposta, servico,
    solicitacao, plano, webhook, usuario_router
)
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

# 1) Descobre a RAIZ do projeto: a pasta que contém "app/"
#    (__file__ → .../app/main.py  →  parent = .../app  →  parent.parent = raiz)
# ────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent   # <- raiz do projeto
UPLOADS_DIR  = PROJECT_ROOT / "uploads"                 # /app/uploads
IMAGENS_DIR  = UPLOADS_DIR / "imagens" / "perfil"       # /app/uploads/imagens/perfil

# Garante que o diretório exista
IMAGENS_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────────────────────
# 2) Faz o mount. Agora qualquer arquivo em /app/uploads/imagens/*
#    será servido em  http://<host>:8000/imagens/…
# ────────────────────────────────────────────────────────────────
app.mount(
    "/imagens",
    StaticFiles(directory=str(UPLOADS_DIR / "imagens")),
    name="imagens",
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
app.include_router(usuario_router.router, tags=["usuarios"])
app.include_router(imagem_routes.router)
app.include_router(webhook.router)
app.include_router(proposta.router)

@app.get("/")
def home():
    return {"msg": "API Center Sew, conexão entre empresas e costureiras"}