from typing import List
from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.servico import Servico
from app.models.solicitacao import Solicitacao
from app.models.usuario import Usuario
from app.schemas.servico_schema import ServicoCreate, ServicoResponse
from app.schemas.usuario_schema import UsuarioResponse
from utils.helpers import build_foto_url


class ServicoService:
    @staticmethod
    async def criar(dados: ServicoCreate) -> ServicoResponse:
        if not all([dados.solicitacao_id, dados.empresa_id, dados.prestador_id]):
            raise HTTPException(400, detail="Campos obrigatórios ausentes.")

        novo_servico = Servico(
            solicitacao_id=dados.solicitacao_id,
            empresa_id=dados.empresa_id,
            prestador_id=dados.prestador_id,
            produto=dados.produto,
            inicio=dados.inicio,
            previsao=dados.previsao,
            status="Em andamento",
        )
        await novo_servico.insert()

        data = novo_servico.dict(by_alias=True)
        data["_id"] = str(data["_id"])

        # Carrega empresa e prestador do banco
        empresa = await Usuario.get(ObjectId(dados.empresa_id))
        prestador = await Usuario.get(ObjectId(dados.prestador_id))

        if not empresa or not prestador:
            raise HTTPException(404, detail="Empresa ou prestador não encontrado.")

        # Monta payload no formato do ServicoResponse
        data["empresa"] = UsuarioResponse(**empresa.dict())
        data["prestador"] = UsuarioResponse(**prestador.dict())

        return ServicoResponse(**data)

    @staticmethod
    async def listar() -> List[ServicoResponse]:
        servicos = await Servico.find_all().to_list()
        respostas: List[ServicoResponse] = []

        for servico in servicos:
            servico_dict = jsonable_encoder(servico, by_alias=True)

            # Título da solicitação
            try:
                solicitacao = await Solicitacao.get(ObjectId(servico.solicitacao_id))
                servico_dict["titulo_solicitacao"] = solicitacao.titulo if solicitacao else None
            except Exception:
                servico_dict["titulo_solicitacao"] = None

            # Empresa
            empresa = await Usuario.get(ObjectId(servico.empresa_id))
            if not empresa:
                continue
            empresa_dict = jsonable_encoder(empresa, by_alias=True)
            empresa_dict["foto_url"] = build_foto_url(empresa_dict.get("foto"))
            servico_dict["empresa"] = UsuarioResponse(**empresa_dict)

            # Prestador
            prestador = await Usuario.get(ObjectId(servico.prestador_id))
            if not prestador:
                continue
            prestador_dict = jsonable_encoder(prestador, by_alias=True)
            prestador_dict["foto_url"] = build_foto_url(prestador_dict.get("foto"))
            servico_dict["prestador"] = UsuarioResponse(**prestador_dict)

            respostas.append(ServicoResponse(**servico_dict))

        return respostas

    @staticmethod
    async def obter_por_id(servico_id: str) -> ServicoResponse:
        servico = await Servico.get(servico_id)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

        servico_dict = jsonable_encoder(servico, by_alias=True)

        # Título da solicitação
        titulo = None
        try:
            solicitacao = await Solicitacao.get(ObjectId(servico.solicitacao_id))
            if solicitacao:
                titulo = solicitacao.titulo
        except Exception:
            pass

        servico_dict["titulo_solicitacao"] = titulo

        # Empresa
        try:
            empresa = await Usuario.get(ObjectId(servico.empresa_id))
            if empresa:
                servico_dict["empresa"] = UsuarioResponse(**jsonable_encoder(empresa, by_alias=True))
        except Exception:
            servico_dict["empresa"] = None

        # Prestador
        try:
            prestador = await Usuario.get(ObjectId(servico.prestador_id))
            if prestador:
                servico_dict["prestador"] = UsuarioResponse(**jsonable_encoder(prestador, by_alias=True))
        except Exception:
            servico_dict["prestador"] = None

        return ServicoResponse(**servico_dict)

    # =========================
    #       NOVOS MÉTODOS
    # =========================

    @staticmethod
    async def atualizar_status(
        servico_id: str,
        novo_status: str,
        solicitante_id: str,  # vem do token (payload["user_id"])
    ) -> dict:
        """
        Atualiza o status do serviço. Se for 'Finalizado', somente o PRESTADOR responsável pode fazê-lo.
        Compatível com rotas que usam JWTBearer + decode_jwt.
        """
        novo_status = (novo_status or "").strip()
        if not novo_status:
            raise HTTPException(status_code=400, detail="status obrigatório")

        servico = await Servico.get(servico_id)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

        # Regra de permissão: somente o prestador responsável pode finalizar
        if novo_status.lower() == "finalizado":
            if str(solicitante_id) != str(servico.prestador_id):
                raise HTTPException(status_code=403, detail="Apenas o prestador responsável pode finalizar o serviço")

        # (Opcional) Whitelist de transições
        # allowed = {"Em andamento", "Pausado", "Finalizado"}
        # if novo_status not in allowed:
        #     raise HTTPException(status_code=400, detail="status inválido")

        await Servico.find_one(Servico.id == servico.id).update_one({"$set": {"status": novo_status}})
        return {"ok": True, "status": novo_status}

    @staticmethod
    async def finalizar(
        servico_id: str,
        solicitante_id: str,
    ) -> dict:
        """
        Atalho para marcar como 'Finalizado'.
        """
        return await ServicoService.atualizar_status(servico_id, "Finalizado", solicitante_id)