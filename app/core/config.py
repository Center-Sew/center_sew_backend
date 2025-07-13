# app/core/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://192.168.15.188:8000")
    MONGO_URL: str = os.getenv("MONGO_URL")
    DATABASE_NAME: str = os.getenv("MONGO_DB_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

settings = Settings()