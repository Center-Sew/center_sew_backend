from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import auth, profile, prestador, servico, solicitacao
from app.database.mongo import init_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo()
    yield

app = FastAPI(lifespan=lifespan)

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(servico.router, prefix="/services", tags=["services"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(prestador.router, prefix="/prestador", tags=["prestador"])
app.include_router(solicitacao.router, prefix="/solicitacoes", tags=["solicitacoes"])

@app.get("/")
def home():
    return {"msg": "API Center Sew, conexão entre empresas e costureiras"}
