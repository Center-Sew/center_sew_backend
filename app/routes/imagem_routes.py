from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from app.core.config import settings

router = APIRouter()

@router.get("/imagens/{nome_arquivo}")
async def servir_imagem(nome_arquivo: str):
    caminho = os.path.join(settings.UPLOAD_DIR, nome_arquivo)
    if os.path.exists(caminho):
        return FileResponse(caminho)
    else:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")