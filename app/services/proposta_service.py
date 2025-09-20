# app/services/proposta_service.py
import json
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException
from bson import ObjectId

from app.models.chat_model import MensagemChat
from app.models.proposta import Proposta          # Model já com prestador_id
from app.models.solicitacao import Solicitacao
from app.models.usuario import Usuario
from app.schemas.proposta_schema import PropostaCreate, PropostaModel, PropostaResponse
from app.schemas.servico_schema import ProdutoSchema, ServicoCreate
from app.services.servico_service import ServicoService
from app.core.config import settings


class PropostaService:

    # ----------------- helpers -----------------
    @staticmethod
    def _resolve_empresa_oid(solicitacao: Solicitacao) -> ObjectId:
        """
        Tenta obter o ObjectId da empresa a partir da solicitação.
        Prioriza solicitacao.empresa_id; como legado, tenta solicitacao.usuario_id.
        """
        raw = getattr(solicitacao, "empresa_id", None) or getattr(solicitacao, "usuario_id", None)
        if not raw:
            raise HTTPException(status_code=400, detail="Solicitação sem empresa vinculada.")
        return raw if isinstance(raw, ObjectId) else ObjectId(str(raw))

    # ----------------- criação -----------------
    @staticmethod
    async def criar(solicitacao_id: str, prestador_id: str, dados: PropostaCreate) -> PropostaModel:
        solicitacao = await Solicitacao.get(ObjectId(solicitacao_id))
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")

        if getattr(solicitacao, "proposta_aceita", False):
            raise HTTPException(status_code=400, detail="Essa solicitação já teve uma proposta aceita.")

        empresa_oid = PropostaService._resolve_empresa_oid(solicitacao)

        proposta = Proposta(
            solicitacao_id=ObjectId(solicitacao_id),
            prestador_id=ObjectId(prestador_id),   # ✅ novo campo
            empresa_id=empresa_oid,
            mensagem=dados.mensagem,
        )

        print("Proposta: ", proposta)
        
        await proposta.insert()

        return PropostaModel.model_validate_json(proposta.model_dump_json(by_alias=True))

    # ----------------- listagem por solicitação -----------------
    @staticmethod
    async def listar_por_solicitacao(solicitacao_id: str, usuario_logado_id: str) -> List[PropostaModel]:
        propostas = await Proposta.find(
            {
                "solicitacao_id": ObjectId(solicitacao_id),
                "status": {"$ne": "recusada"},
            }
        ).sort("-data_envio").to_list()

        resultado: List[PropostaModel] = []

        for proposta in propostas:
            # ⚠️ antes: proposta.usuario_id
            autor = await Usuario.get(proposta.prestador_id)
            if not autor:
                raise HTTPException(status_code=404, detail="Usuário autor da proposta não encontrado.")

            proposta_data = json.loads(proposta.model_dump_json(by_alias=True))
        
            # bloco 'usuario' (opcional/legado) – mantém compat com front
            proposta_data["usuario"] = {
                "id": str(autor.id),
                "nome": autor.nome,
                "email": autor.email,
                "foto": f"{settings.BACKEND_URL}/imagens/perfil/{autor.foto}" if autor.foto else None,
            }

            mensagens_nao_lidas = await MensagemChat.find({
                "proposta_id": ObjectId(proposta.id),
                "destinatario_id": ObjectId(usuario_logado_id),
                "remetente_id": {"$ne": ObjectId(usuario_logado_id)},
                "lido": False
            }).count()

            proposta_data["possui_mensagem_nova"] = mensagens_nao_lidas > 0

            resultado.append(PropostaModel.model_validate_json(json.dumps(proposta_data)))

        return resultado

    # ----------------- listar do prestador -----------------
    @staticmethod
    async def buscar_propostas_do_prestador(solicitacao_id: str, prestador_id: str) -> List[PropostaResponse]:
        propostas = await Proposta.find(
            Proposta.solicitacao_id == ObjectId(solicitacao_id),
            Proposta.prestador_id == ObjectId(prestador_id)
        ).to_list()

        resultados: List[PropostaResponse] = []
        for p in propostas:
            proposta_data = json.loads(p.model_dump_json(by_alias=True))

            mensagens_nao_lidas = await MensagemChat.find({
                "proposta_id": p.id,
                "destinatario_id": ObjectId(prestador_id),
                "remetente_id": {"$ne": ObjectId(prestador_id)},
                "lido": False
            }).count()

            proposta_data["possui_mensagem_nova"] = mensagens_nao_lidas > 0
            resultados.append(PropostaResponse.model_validate_json(json.dumps(proposta_data)))

        return resultados

    # -------------- aceitar / rejeitar --------------
    @staticmethod
    async def aceitar_proposta(solicitacao_id: str, proposta_id: str, usuario_logado_id: str):
        proposta = await Proposta.get(proposta_id)
        if not proposta:
            raise HTTPException(status_code=404, detail="Proposta não encontrada")

        # Apenas a empresa dona da solicitação pode aceitar
        if str(proposta.empresa_id) != usuario_logado_id:
            raise HTTPException(status_code=403, detail="Você não tem permissão para aceitar esta proposta")

        # Atualiza proposta aceita
        proposta.status = "aceita"
        await proposta.save()

        # Outras propostas da mesma solicitação -> recusadas
        await Proposta.find({
            "solicitacao_id": ObjectId(solicitacao_id),
            "_id": {"$ne": ObjectId(proposta_id)}
        }).update({"$set": {"status": "recusada"}})

        # Atualiza solicitação
        solicitacao = await Solicitacao.get(ObjectId(solicitacao_id))
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")

        solicitacao.proposta_aceita = True
        solicitacao.status = "Em andamento"
        await solicitacao.save()

        # Cria Serviço (empresa = dona da solicitação; prestador = quem fez a proposta aceita)
        empresa_oid = PropostaService._resolve_empresa_oid(solicitacao)

        servico_data = ServicoCreate(
            solicitacao_id=solicitacao_id,
            empresa_id=str(empresa_oid),
            prestador_id=str(proposta.prestador_id),   # ✅ antes era proposta.usuario_id
            produto=ProdutoSchema(nome="Serviço contratado", quantidade=1),
            inicio=datetime.utcnow(),
            previsao=datetime.utcnow() + timedelta(days=7),
        )
        await ServicoService.criar(servico_data)

        return {"detail": "Proposta aceita com sucesso"}

    @staticmethod
    async def rejeitar_proposta(solicitacao_id: str, proposta_id: str, usuario_id: str):
        solicitacao_obj_id = ObjectId(solicitacao_id)
        proposta_obj_id = ObjectId(proposta_id)

        solicitacao = await Solicitacao.get(solicitacao_obj_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")

        # Apenas a empresa dona pode rejeitar
        if str(PropostaService._resolve_empresa_oid(solicitacao)) != usuario_id:
            raise HTTPException(status_code=403, detail="Acesso negado")

        proposta = await Proposta.find_one(
            Proposta.id == proposta_obj_id,
            Proposta.solicitacao_id == solicitacao_obj_id
        )
        if not proposta:
            raise HTTPException(status_code=404, detail="Proposta não encontrada")

        await Proposta.find_one(Proposta.id == proposta_obj_id).update({"$set": {"status": "recusada"}})
        return {"mensagem": "Proposta recusada com sucesso!"}

    # -------------- contagem de interessados --------------
    @staticmethod
    async def contar_interessados_unicos(solicitacao_id: str) -> int:
        propostas = await Proposta.find(Proposta.solicitacao_id == ObjectId(solicitacao_id)).to_list()
        # ⚠️ antes: usuario_id
        prestador_ids = {p.prestador_id for p in propostas if getattr(p, "prestador_id", None)}
        return len(prestador_ids)

    # (legado) alias para não quebrar chamadas antigas
    @staticmethod
    async def buscar_propostas_do_usuario(solicitacao_id: str, usuario_id: str) -> List[PropostaResponse]:
        return await PropostaService.buscar_propostas_do_prestador(solicitacao_id, usuario_id)
