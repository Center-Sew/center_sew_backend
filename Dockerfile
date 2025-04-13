# Base image
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando padrão (produção)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
