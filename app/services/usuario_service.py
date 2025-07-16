from app.models.usuario import Usuario
from bson import ObjectId
from fastapi import HTTPException, UploadFile
from uuid import uuid4
import os, shutil
from app.core.config import settings


class UsuarioService:
    EXTENSOES_VALIDAS = {".jpg", ".jpeg", ".png"}

    @staticmethod
    async def atualizar_foto(usuario_id: str, arquivo: UploadFile) -> str:
        # 1️⃣ valida extensão
        ext = os.path.splitext(arquivo.filename)[-1].lower()
        if ext not in UsuarioService.EXTENSOES_VALIDAS:
            raise HTTPException(400, "Formato de imagem inválido")

        # 2️⃣ nome e salvamento no subdiretório "imagens/perfil/"
        nome_arquivo = f"{uuid4().hex}{ext}"
        pasta_perfil = os.path.join(settings.UPLOAD_DIR, "imagens", "perfil")
        os.makedirs(pasta_perfil, exist_ok=True)

        caminho = os.path.join(pasta_perfil, nome_arquivo)
        with open(caminho, "wb") as buf:
            shutil.copyfileobj(arquivo.file, buf)

        # 3️⃣ monta URL pública para retornar na resposta (mas não salva no banco)
        url_foto = f"{settings.BACKEND_URL}/imagens/perfil/{nome_arquivo}"

        # 4️⃣ Beanie: buscar e atualizar
        usuario = await Usuario.get(ObjectId(usuario_id))
        if not usuario:
            raise HTTPException(404, "Usuário não encontrado")

        usuario.foto = nome_arquivo  # ✅ salva apenas o nome
        await usuario.save()

        return url_foto