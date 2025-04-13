from jose import jwt
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