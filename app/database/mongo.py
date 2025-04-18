from pymongo import MongoClient
import os
from dotenv import load_dotenv
from app.auth.auth_handler import hash_password
from faker import Faker
import random
from datetime import datetime

load_dotenv()

# Conexão com MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client["centersew"]

# 🔁 Limpar coleções antes de inserir novamente
db.users.delete_many({})
db.solicitacoes.delete_many({})

# 👤 Inserir usuários
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
user_ids = db.users.insert_many(users).inserted_ids

# 📦 Dados de base
fake = Faker("pt_BR")

tipos_servico = [
    "Ajuste de uniforme", "Reparo de jaleco", "Bordado de logotipo",
    "Confecção de aventais", "Costura de cortina", "Bainha de calça",
    "Troca de zíper", "Aplicação de patches", "Uniformes hospitalares",
    "Costura de capa para máquina"
]

descricoes_base = [
    "Ajustar tamanho para conforto no ambiente de trabalho.",
    "Costura fina com acabamento reforçado.",
    "Aplicar bordado com logotipo da empresa.",
    "Reparo urgente solicitado pelo setor de engenharia.",
    "Solicitação recorrente da equipe de manutenção.",
    "Confecção com tecido fornecido pela empresa.",
    "Padronização de jalecos do laboratório.",
    "Serviço de urgência para visita de auditoria.",
    "Tecido frágil, exige cuidado especial.",
    "Acabamento interno deve ser em viés colorido."
]

localizacoes_alvo = [
    {"tipo": "cidade", "valor": "São Paulo"},
    {"tipo": "raio", "valor": "20km"},
    {"tipo": "estado", "valor": "SP"},
    {"tipo": "raio", "valor": "50km"},
    {"tipo": "cidade", "valor": "Campinas"},
]

solicitacoes = []

for i in range(1, 51):  # 50 registros
    tipo = random.choice(tipos_servico)
    descricao = random.choice(descricoes_base)
    localizacao = random.choice(localizacoes_alvo)
    empresa_id = random.choice(user_ids)

    solicitacoes.append({
        "titulo": f"Solicitação #{i:03}",
        "descricao": tipo,
        "empresa_id": str(empresa_id),
        "data_criacao": datetime.utcnow().isoformat(),
        "status": "aberta",
        "interessados": [],  # Inicialmente sem interessados
        "perfil_desejado": {
            "tipo_fiscal": random.sample(["CPF", "CNPJ"], k=random.choice([1, 2])),
            "tipo_servico": tipo,
            "descricao": descricao,
            "localizacao_alvo": localizacao
        }
    })

db.solicitacoes.insert_many(solicitacoes)

print("✅ Seed concluído com sucesso com estrutura atualizada.")