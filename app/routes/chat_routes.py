from fastapi import APIRouter, Depends
from typing import List
from app.schemas.chat_schema import MensagemCreate, MensagemResponse
from app.services.chat_service import ChatService
from app.auth.auth_bearer import JWTBearer
from app.security.rbac import role_required

router = APIRouter(prefix="/chat", tags=["Chat"])

# Enviar mensagem (empresa e prestador podem enviar)
@router.post("/mensagem", response_model=MensagemResponse)
async def enviar_mensagem(
    mensagem: MensagemCreate,
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    resultado = await ChatService.enviar_mensagem(
        proposta_id=mensagem.proposta_id,
        remetente_id=token_payload["sub"],
        destinatario_id=mensagem.destinatario_id,
        texto=mensagem.texto
    )
    return MensagemResponse(**resultado.model_dump(by_alias=True))

# Listar mensagens por proposta (empresa e prestador podem ver)
@router.get("/mensagens/{proposta_id}", response_model=List[MensagemResponse])
async def listar_mensagens(
    proposta_id: str,
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    mensagens = await ChatService.listar_mensagens(proposta_id, token_payload["sub"])
    return [MensagemResponse(**m.model_dump(by_alias=True)) for m in mensagens]

# Marcar mensagens como lidas (empresa e prestador)
@router.put("/mensagens/lidas/{proposta_id}")
async def marcar_lidas(
    proposta_id: str,
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    await ChatService.marcar_como_lidas(proposta_id, token_payload["sub"])
    return {"status": "ok"}