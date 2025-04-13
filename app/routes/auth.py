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
        return { "access_token": sign_jwt(str(user.email)) }
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

