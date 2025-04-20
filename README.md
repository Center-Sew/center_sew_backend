# 🧵 Conecta Costura - Backend

API robusta em **FastAPI** + **MongoDB** que conecta empresas e prestadores de serviços de costura. Implementa autenticação segura, gerenciamento de solicitações e perfis, com estrutura modular e escalável.

---

## ✅ Funcionalidades

- 🔐 Autenticação segura com JWT (expiração configurável)
- 🧾 CRUD completo de solicitações de serviço
- 🎯 Seleção por perfil desejado (CPF, CNPJ e tipo de serviço)
- 🧍 Adição de interessados (usuários) em cada solicitação
- ⏱ Status da solicitação: `aberta`, `em_andamento`, `concluída`, `atrasada`
- 👤 Gerenciamento de perfil do usuário logado
- 🧑‍🔧 Consulta de prestadores com filtros geográficos

---

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── main.py
│   ├── auth/
│   │   ├── auth_handler.py          # Criação e verificação de JWT com expiração
│   │   └── auth_bearer.py           # Middleware de autenticação JWT
│   ├── database/
│   │   └── mongo.py                 # Conexão Beanie + Motor (MongoDB async)
│   ├── models/
│   │   ├── usuario.py               # Modelo base de usuário
│   │   ├── solicitacao.py           # Modelo de solicitação (Beanie)
│   │   ├── prestador.py             # Prestador de serviço
│   │   ├── perfil_desejado.py       # Perfil fiscal, serviço e localização
│   │   └── localizacao.py           # Submodelo de localização alvo
│   ├── routes/
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── prestador.py
│   │   ├── servico.py
│   │   └── solicitacao.py
│   ├── schemas/
│   │   ├── usuario_schema.py
│   │   ├── solicitacao_schema.py
│   │   └── prestador_schema.py
│   └── services/
│       └── solicitacao_service.py   # Lógica de negócios da solicitação
├── seeds/
│   ├── usuario_seed.py
│   ├── solicitacao_seed.py
│   └── data/                        # Dados JSON utilizados pelos seeds
├── cli.py                           # Script de CLI para rodar seeds
├── .env                             # Variáveis de ambiente
└── requirements.txt
```

---

## ⚙️ Execução

### 1. Clone e entre no projeto

```bash
git clone https://github.com/seu-usuario/conecta-costura-backend.git
cd conecta-costura-backend
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o `.env`

```env
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=centersew
SECRET_KEY=sua_chave_supersecreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

Abra: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Autenticação

- Os tokens JWT têm tempo de expiração (`exp`) e devem ser usados no header:

```http
Authorization: Bearer <token>
```

---

## 🧪 Exemplos de Requisições

### 🔑 Registro / Login

```json
# POST /auth/register
{
  "nome": "Empresa XPTO",
  "email": "empresa@xpto.com",
  "senha": "123456",
  "tipo": "empresa",
  "documento": "12.345.678/0001-90",
  "localizacao": {
    "cidade": "São Paulo",
    "estado": "SP",
    "bairro": "Centro",
    "tipo": "cidade",
    "valor": "São Paulo"
  }
}

# POST /auth/login
{
  "email": "empresa@xpto.com",
  "senha": "123456"
}
```

### 📋 Criar solicitação

```json
# POST /solicitacoes/
{
  "titulo": "Uniformes para evento",
  "descricao": "Preciso de 30 camisetas personalizadas com logo bordado",
  "perfil_desejado": {
    "tipo_fiscal": ["CPF", "CNPJ"],
    "tipo_servico": "Bordado de logotipo",
    "descricao": "Experiência em bordados detalhados",
    "localizacao_alvo": {
      "cidade": "São Paulo",
      "estado": "SP",
      "bairro": "Bela Vista",
      "tipo": "bairro",
      "valor": "Bela Vista"
    }
  }
}
```

---

## 🧰 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB + Beanie ODM](https://roman-right.github.io/beanie/)
- [JWT](https://jwt.io/)
- [Uvicorn](https://www.uvicorn.org/)
- [Typer](https://typer.tiangolo.com/) (para CLI de seeds)
- [Pydantic v2](https://docs.pydantic.dev/) com aliases e validação de enums

---

## 🔍 Organização de código

- Arquitetura desacoplada com `routes`, `services`, `models`, `schemas`
- Suporte a múltiplos tipos de usuários (empresa, prestador)
- Seeds automáticos com JSON estruturado
- Uso de enums (`TipoServico`, `TipoFiscal`, `TipoLocalizacaoAlvo`) padronizados

---

## 📌 Melhorias Futuras

- Match de prestadores baseado em geolocalização
- Avaliações e comentários
- Upload de portfólio e imagens
- Filtros avançados por localização, tipo fiscal e tipo de serviço