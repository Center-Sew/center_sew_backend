from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import ExpiredSignatureError, jwt, JWTError
from dotenv import load_dotenv
import os

# 🔐 Carregar variáveis do .env
load_dotenv()

# ✅ Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "fallbacksecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 🔒 Contexto de criptografia para senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Hashear senha (para cadastro ou seed)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Verificar senha (para login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Criar token JWT com expiração
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Decodificar token com tratamento
def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")