from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from fastapi import HTTPException
from app.models.chat_model import MensagemChat
from app.models.proposta import Proposta

class ChatService:

    @staticmethod
    async def enviar_mensagem(proposta_id: str, remetente_id: str, destinatario_id: str, texto: str):
        mensagem = MensagemChat(
            proposta_id=ObjectId(proposta_id),
            remetente_id=ObjectId(remetente_id),
            destinatario_id=ObjectId(destinatario_id),
            texto=texto,
            lida=False,
            data_envio=datetime.now(timezone.utc),
        )
        await mensagem.insert()
        return mensagem

    @staticmethod
    async def listar_mensagens(proposta_id: str, usuario_id: str) -> List[MensagemChat]:
        proposta = await Proposta.get(ObjectId(proposta_id))
        if not proposta:
            raise HTTPException(status_code=404, detail="Proposta não encontrada")

        if str(proposta.usuario_id) != usuario_id and str(proposta.empresa_id) != usuario_id:
            raise HTTPException(status_code=403, detail="Acesso negado à proposta")

        return await MensagemChat.find({"proposta_id": ObjectId(proposta_id)}).sort("timestamp").to_list()


    @staticmethod
    async def marcar_como_lidas(proposta_id: str, usuario_id: str):
        await MensagemChat.find(
            {
                "proposta_id": ObjectId(proposta_id),
                "destinatario_id": ObjectId(usuario_id),
                "lido": False
            }
        ).update({"$set": {"lido": True}})