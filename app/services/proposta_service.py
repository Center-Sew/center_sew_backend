import asyncio
import json
from typing import List

from fastapi import HTTPException
from app.models.chat_model import MensagemChat
from app.models.proposta import Proposta
from app.models.solicitacao import Solicitacao
from app.models.usuario import Usuario
from app.schemas.proposta_schema import PropostaCreate, PropostaModel
from app.core.config import settings

from bson import ObjectId
from app.models.usuario import Usuario

class PropostaService:

    from bson import ObjectId

    @staticmethod
    async def criar(solicitacao_id: str, usuario_id: str, dados: PropostaCreate) -> PropostaModel:
        solicitacao = await Solicitacao.get(ObjectId(solicitacao_id))
        if not solicitacao:
            raise HTTPException(404, "Solicitação não encontrada")

        proposta = Proposta(
            solicitacao_id=ObjectId(solicitacao_id),
            usuario_id=ObjectId(usuario_id),
            empresa_id=solicitacao.usuario_id,  # já é ObjectId
            mensagem=dados.mensagem,
        )

        await proposta.insert()
        return PropostaModel.model_validate_json(proposta.model_dump_json(by_alias=True))

    @staticmethod
    async def listar_por_solicitacao(solicitacao_id: str) -> List[PropostaModel]:
        propostas = await Proposta.find(
            Proposta.solicitacao_id == ObjectId(solicitacao_id)
        ).sort("-data_envio").to_list()

        resultado = []

        for proposta in propostas:
            autor = await Usuario.get(proposta.usuario_id)
            if not autor:
                raise HTTPException(404, "Usuário autor da proposta não encontrado.")

            # Serializa corretamente
            proposta_data = json.loads(proposta.model_dump_json(by_alias=True))

            proposta_data["usuario"] = {
                "id": str(autor.id),
                "nome": autor.nome,
                "email": autor.email,
                "foto": f"{settings.BACKEND_URL}/imagens/perfil/{autor.foto}" if autor.foto else None,
            }

            mensagens_nao_lidas = await MensagemChat.find({
                "proposta_id": proposta.id,
                "destinatario_id": proposta.empresa_id,
                "lido": False
            }).count()

            proposta_data["possui_mensagem_nova"] = mensagens_nao_lidas > 0

            resultado.append(PropostaModel.model_validate_json(json.dumps(proposta_data)))

        return resultado

    @staticmethod
    async def buscar_propostas_do_usuario(solicitacao_id: str, usuario_id: str) -> list[PropostaModel]:
        propostas = await Proposta.find(
            Proposta.solicitacao_id == ObjectId(solicitacao_id),
            Proposta.usuario_id == ObjectId(usuario_id)
        ).to_list()

        
        resultados = []
        for p in propostas:
            # dump do documento como JSON (já serializa ObjectId para str)
            proposta_json_str = p.model_dump_json(by_alias=True)
            proposta_data = json.loads(proposta_json_str)

            # opcional: enriquecer com dados do usuário
            usuario = await Usuario.get(p.usuario_id)

            proposta_data["usuario"] = {
                "id": str(usuario.id),
                "nome": usuario.nome,
                "email": usuario.email,
                "foto": f"{settings.BACKEND_URL}/imagens/perfil/{usuario.foto}" if usuario.foto else None,
            }

            mensagens_nao_lidas = await MensagemChat.find({
                "proposta_id": p.id,
                "destinatario_id": ObjectId(usuario_id),
                "lido": False
            }).count()

            proposta_data["possui_mensagem_nova"] = mensagens_nao_lidas > 0

            resultados.append(PropostaModel.model_validate_json(json.dumps(proposta_data)))

        return resultados

    @staticmethod
    async def aceitar_proposta(solicitacao_id: str, proposta_id: str, usuario_id: str):
        from bson import ObjectId

        solicitacao_obj_id = ObjectId(solicitacao_id)
        proposta_obj_id = ObjectId(proposta_id)

        # Verifica se a solicitação pertence ao usuário logado
        solicitacao = await Solicitacao.get(solicitacao_obj_id)
        if not solicitacao:
            raise HTTPException(404, "Solicitação não encontrada")
        if str(solicitacao.usuario_id) != usuario_id:
            raise HTTPException(403, "Acesso negado")

        # Busca todas as propostas da solicitação (somente _id)
        propostas_ids = await Proposta.find(
            Proposta.solicitacao_id == solicitacao_obj_id
        ).project({"_id": 1}).to_list()

        if not any(p["_id"] == proposta_obj_id for p in propostas_ids):
            raise HTTPException(404, "Proposta não encontrada")

        # Atualiza status de cada proposta individualmente
        for p in propostas_ids:
            prop = await Proposta.get(p["_id"])
            if not prop:
                continue

            novo_status = "aceita" if prop.id == proposta_obj_id else "recusada"

            if prop.status != novo_status:
                prop.status = novo_status
                await prop.save()

        return {"mensagem": "Proposta aceita com sucesso!"}
    
    @staticmethod
    async def rejeitar_proposta(solicitacao_id: str, proposta_id: str, usuario_id: str):
        from bson import ObjectId

        solicitacao_obj_id = ObjectId(solicitacao_id)
        proposta_obj_id = ObjectId(proposta_id)

        solicitacao = await Solicitacao.get(solicitacao_obj_id)
        if not solicitacao:
            raise HTTPException(404, "Solicitação não encontrada")
        if str(solicitacao.usuario_id) != usuario_id:
            raise HTTPException(403, "Acesso negado")

        proposta = await Proposta.find_one(
            Proposta.id == proposta_obj_id,
            Proposta.solicitacao_id == solicitacao_obj_id
        )
        if not proposta:
            raise HTTPException(404, "Proposta não encontrada")

        await Proposta.find_one(Proposta.id == proposta_obj_id).update({"$set": {"status": "recusada"}})

        return {"mensagem": "Proposta recusada com sucesso!"}

    @staticmethod
    async def contar_interessados_unicos(solicitacao_id: str) -> int:
        propostas = await Proposta.find(Proposta.solicitacao_id == ObjectId(solicitacao_id)).to_list()
        print("Interessados: ", propostas)
        usuario_ids = {p.usuario_id for p in propostas}
        return len(usuario_ids)