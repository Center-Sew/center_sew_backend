# Estrutura completa do backend com FastAPI, MongoDB, JWT e boas práticas

# Requisitos
# - Autenticação segura por email/senha (JWT)
# - CRUD de solicitações de serviço
# - Acompanhamento de status: Em andamento, Concluído, Atrasado
# - Detalhes de prestadores de serviço
# - Perfil da conta atual com segurança

# Estrutura do projeto
# backend/
# ├── app/
# │   ├── main.py
# │   ├── auth/
# │   │   ├── auth_handler.py
# │   │   └── auth_bearer.py
# │   ├── database/
# │   │   └── mongo.py
# │   ├── models/
# │   │   ├── user.py
# │   │   ├── service.py
# │   │   └── prestador.py
# │   ├── routes/
# │   │   ├── auth.py
# │   │   ├── services.py
# │   │   ├── profile.py
# │   │   └── prestador.py
# └── requirements.txt

# app/main.py
from fastapi import FastAPI
from app.routes import auth, services, profile, prestador

app = FastAPI()

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(prestador.router, prefix="/prestador", tags=["prestador"])

@app.get("/")
def home():
    return {"msg": "API Conecta Costura"}

# app/auth/auth_handler.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "supersecret"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def sign_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

# app/auth/auth_bearer.py
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

# app/models/user.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr

# app/models/service.py
from pydantic import BaseModel
from typing import Optional

class ServiceRequest(BaseModel):
    titulo: str
    subtitulo: str
    descricao: str
    status: str = "Em andamento"
    user_id: Optional[str]

# app/models/prestador.py
from pydantic import BaseModel

class PrestadorDetalhe(BaseModel):
    nome: str
    especialidade: str
    localizacao: str

# app/database/mongo.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["costura"]

# app/routes/auth.py
from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.auth.auth_handler import sign_jwt, hash_password, verify_password
from app.database.mongo import db

router = APIRouter()

@router.post("/register")
def register(user: User):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    db.users.insert_one(user_dict)
    return sign_jwt(str(user.email))

@router.post("/login")
def login(user: User):
    db_user = db.users.find_one({"email": user.email})
    if db_user and verify_password(user.password, db_user["password"]):
        return sign_jwt(str(user.email))
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

# app/routes/services.py
from fastapi import APIRouter, Depends
from app.models.service import ServiceRequest
from app.auth.auth_bearer import JWTBearer
from app.database.mongo import db

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())])
def criar_servico(service: ServiceRequest):
    db.services.insert_one(service.dict())
    return {"msg": "Serviço criado com sucesso"}

@router.get("/", dependencies=[Depends(JWTBearer())])
def listar_servicos():
    return list(db.services.find({}, {"_id": 0}))

@router.get("/{titulo}", dependencies=[Depends(JWTBearer())])
def buscar_por_titulo(titulo: str):
    return db.services.find_one({"titulo": titulo}, {"_id": 0})

# app/routes/profile.py
from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt
from fastapi import Request
from app.database.mongo import db

router = APIRouter()

@router.get("/me", dependencies=[Depends(JWTBearer())])
def meu_perfil(request: Request):
    token = request.headers.get("Authorization").split(" ")[1]
    payload = decode_jwt(token)
    user = db.users.find_one({"email": payload["user_id"]}, {"_id": 0, "password": 0})
    return user

# app/routes/prestador.py
from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.database.mongo import db

router = APIRouter()

@router.get("/{nome}", dependencies=[Depends(JWTBearer())])
def detalhes_prestador(nome: str):
    return db.prestadores.find_one({"nome": nome}, {"_id": 0})
