from datetime import datetime, timezone
from typing import List, Literal, Optional
from bson import ObjectId
from fastapi import HTTPException

from app.models.chat_model import MensagemChat
from app.models.proposta import Proposta
from app.models.servico import Servico


class ChatService:

    @staticmethod
    async def enviar_mensagem(
        proposta_id: Optional[str] = None,
        servico_id: Optional[str] = None,
        remetente_id: str = "",
        destinatario_id: str = "",
        texto: str = ""
    ) -> MensagemChat:
        if not proposta_id and not servico_id:
            raise HTTPException(status_code=400, detail="proposta_id ou servico_id obrigatório")

        print("Eu estou aqui!")

        dados = {
            "remetente_id": ObjectId(remetente_id),
            "destinatario_id": ObjectId(destinatario_id),
            "texto": texto,
            "lido": False,
            "data_envio": datetime.now(timezone.utc),
        }

        print("Enviar: ", dados)

        if proposta_id:
            dados["proposta_id"] = ObjectId(proposta_id)

        if servico_id:
            dados["servico_id"] = ObjectId(servico_id)

        mensagem = MensagemChat(**dados)
        await mensagem.insert()
        return mensagem

    @staticmethod
    async def listar_mensagens(
        origem: Literal["proposta", "servico"],
        origem_id: ObjectId,
        empresa_id: ObjectId,
        prestador_id: ObjectId
    ) -> List[MensagemChat]:
        """
        Lista mensagens entre empresa e prestador para a origem informada,
        garantindo que a origem pertença exatamente a esse par.
        """

        # 1) Verifica a origem e pertencimento
        if origem == "proposta":
            proposta = await Proposta.get(origem_id)
            if not proposta:
                raise HTTPException(status_code=404, detail="Proposta não encontrada")

            # proposta.usuario_id pode ser o prestador que enviou, e empresa_id da proposta é a empresa dona
            if (ObjectId(proposta.empresa_id) != empresa_id) or (ObjectId(proposta.prestador_id) != prestador_id):
                raise HTTPException(status_code=403, detail="Proposta não pertence aos participantes informados")

            filtro_origem = {"proposta_id": origem_id}

        elif origem == "servico":
            servico = await Servico.get(origem_id)
            if not servico:
                raise HTTPException(status_code=404, detail="Serviço não encontrado")

            if (ObjectId(servico.empresa_id) != empresa_id) or (ObjectId(servico.prestador_id) != prestador_id):
                raise HTTPException(status_code=403, detail="Serviço não pertence aos participantes informados")

            filtro_origem = {"servico_id": origem_id}

        else:
            raise HTTPException(status_code=400, detail="Origem inválida")

        # 2) Busca apenas conversas entre estes dois participantes (ida e volta)
        filtro_participantes = {
            "$or": [
                {"remetente_id": empresa_id,   "destinatario_id": prestador_id},
                {"remetente_id": prestador_id, "destinatario_id": empresa_id},
            ]
        }

        filtro = {**filtro_origem, **filtro_participantes}

        # 3) Ordena por timestamp crescente (compatível com o seu fromJson)
        return await MensagemChat.find(filtro).sort("data_envio").to_list()

    @staticmethod
    async def marcar_como_lidas(
        proposta_id: Optional[str] = None,
        servico_id: Optional[str] = None,
        usuario_id: str = ""
    ):
        if not proposta_id and not servico_id:
            raise HTTPException(status_code=400, detail="proposta_id ou servico_id obrigatório")

        filtro = {
            "destinatario_id": ObjectId(usuario_id),
            "lido": False
        }

        if proposta_id:
            filtro["proposta_id"] = ObjectId(proposta_id)
        if servico_id:
            filtro["servico_id"] = ObjectId(servico_id)

        print("[Filtro de mensagens não lidas]", filtro)

        mensagens_antes = await MensagemChat.find(filtro).to_list()
        print(f"[ANTES] Encontradas {len(mensagens_antes)} mensagens não lidas")

        result = await MensagemChat.find(filtro).update_many({"$set": {"lido": True}})
        print(f"[UPDATE] {result.modified_count} mensagens atualizadas")

        mensagens_depois = await MensagemChat.find(filtro).to_list()
        print(f"[DEPOIS] Restaram {len(mensagens_depois)} mensagens não lidas")