from fastapi import FastAPI
from app.routes import auth, services, profile, prestador, solicitacao

app = FastAPI()

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(prestador.router, prefix="/prestador", tags=["prestador"])
app.include_router(solicitacao.router, prefix="/solicitacoes", tags=["solicitacoes"])

@app.get("/")
def home():
    return {"msg": "API Center Sew, conexão entre empresas e costureiras"}