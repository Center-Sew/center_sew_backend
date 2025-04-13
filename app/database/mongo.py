from pymongo import MongoClient
import os
from dotenv import load_dotenv
from app.auth.auth_handler import hash_password

load_dotenv()

# Conexão com MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client["centersew"]

# 🔁 Limpar coleções antes de inserir novamente
db.users.delete_many({})
db.solicitacoes.delete_many({})

# 👤 Coleção: users
users = [
    {
        "email": "usuario1@exemplo.com",
        "password": hash_password("123456")
    },
    {
        "email": "costureira@centersew.com",
        "password": hash_password("senha123")
    }
]
db.users.insert_many(users)

# 🧵 Coleção: solicitacoes
solicitacoes = [
    {
        "titulo": "Solicitação #001",
        "subtitulo": "Ajuste de uniforme",
        "descricao": "Costura na barra da calça do setor de produção.",
        "interessados": 3
    },
    {
        "titulo": "Solicitação #002",
        "subtitulo": "Reparo de jaleco",
        "descricao": "Remendo no bolso esquerdo do jaleco do laboratório.",
        "interessados": 1
    },
    {
        "titulo": "Solicitação #003",
        "subtitulo": "Bordado de logotipo",
        "descricao": "Aplicação de logotipo nas camisas do time comercial.",
        "interessados": 5
    },
    {
        "titulo": "Solicitação #004",
        "subtitulo": "Confecção de aventais",
        "descricao": "Criação de aventais personalizados para cozinha industrial.",
        "interessados": 2
    },
]
db.solicitacoes.insert_many(solicitacoes)

print("Seed concluído com sucesso.")
