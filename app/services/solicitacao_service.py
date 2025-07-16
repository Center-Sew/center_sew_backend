from typing import List
from uuid import uuid4
import os, shutil
from bson import ObjectId
from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.models.usuario import Usuario
from app.models.solicitacao import Solicitacao
from app.schemas.solicitacao_schema import SolicitationCreate, SolicitationModel
from app.schemas.usuario_schema import UsuarioPayload


class SolicitacaoService:

    @staticmethod
    async def listar(usuario: dict, pagina: int = 1, tamanho: int = 10) -> List[SolicitationModel]:
        skip = (pagina - 1) * tamanho
        from bson import ObjectId

        filtro = {"usuario_id": ObjectId(usuario["sub"])} if usuario["tipo"] == "empresa" else {"status": "aberta"}

        print("Filtro aplicado:", usuario)


        docs = (
            await Solicitacao.find(filtro)
            .sort("-data_criacao")
            .skip(skip)
            .limit(tamanho)
            .to_list()
        )

        solicitacoes: List[SolicitationModel] = []
        from app.services.proposta_service import PropostaService

        for doc in docs:
            print("Sou doc: ", doc)
            autor = await Usuario.get(doc.usuario_id)
            if not autor:
                raise HTTPException(404, "Usuário (autor) não encontrado")

            data = doc.model_dump()
            data["usuario_id"] = str(doc.usuario_id)
            data["usuario"] = {
                "id": str(autor.id),
                "nome": autor.nome,
                "email": autor.email,
                "segmento": autor.segmento,
                "localizacao": autor.localizacao.dict(),
            }
            data["imagens"] = [f"{settings.BACKEND_URL}/imagens/solicitacoes/{n}" for n in doc.imagens or []]
            data["interessados"] = await PropostaService.contar_interessados_unicos(str(doc.id))
            solicitacoes.append(SolicitationModel(**data))

        return solicitacoes

    @staticmethod
    async def obter_por_id(solicitacao_id: str) -> SolicitationModel:
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(404, "Solicitação não encontrada")

        autor = await Usuario.get(doc.usuario_id)
        if not autor:
            raise HTTPException(404, "Usuário (autor) não encontrado")

        data = doc.model_dump()
        data["usuario"] = {
            "id": str(autor.id),
            "nome": autor.nome,
            "email": autor.email,
            "segmento": autor.segmento,
            "localizacao": autor.localizacao,
        }
        data["imagens"] = [f"{settings.BACKEND_URL}/imagens/solicitacoes/{n}" for n in doc.imagens or []]

        return SolicitationModel(**data)

    @staticmethod
    async def criar(dados: SolicitationCreate, usuario_id: str, arquivos: List[UploadFile] = []) -> SolicitationModel:
        nomes = []

        # Pasta destino: uploads/imagens/solicitacoes
        pasta_destino = os.path.join(settings.UPLOAD_DIR, "imagens", "solicitacoes")
        os.makedirs(pasta_destino, exist_ok=True)

        for arq in arquivos:
            ext = os.path.splitext(arq.filename)[-1]
            nome = f"{uuid4().hex}{ext}"

            caminho_arquivo = os.path.join(pasta_destino, nome)
            with open(caminho_arquivo, "wb") as buf:
                shutil.copyfileobj(arq.file, buf)

            nomes.append(nome)

        nova = Solicitacao(
            **dados.model_dump(),
            usuario_id=ObjectId(usuario_id),
            status="aberta",
            interessados=0,
            imagens=nomes
        )
        await nova.insert()

        autor = await Usuario.get(nova.usuario_id)
        return SolicitationModel(
            **nova.model_dump(exclude={"usuario_id"}),
            usuario_id=str(nova.usuario_id),
            usuario={
                "id": str(autor.id),
                "nome": autor.nome,
                "email": autor.email,
                "segmento": autor.segmento,
                "localizacao": autor.localizacao.dict() if hasattr(autor.localizacao, "dict") else autor.localizacao,
            }
        )