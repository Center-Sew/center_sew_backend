from fastapi import APIRouter, UploadFile, File, Depends
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decode_jwt
from app.services.usuario_service import UsuarioService

router = APIRouter()

@router.patch("/usuarios/foto-perfil")
async def upload_foto_perfil(
    file: UploadFile = File(...),
    token=Depends(JWTBearer())  # ✅ JWT bruto
):
    payload = decode_jwt(token)  # ✅ decode dentro do endpoint
    usuario_id = payload.get("user_id") or payload.get("sub")  # você pode adaptar conforme o JWT real
    return {"foto_url": await UsuarioService.atualizar_foto(usuario_id, file)}