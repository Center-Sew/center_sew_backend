import os
import pprint
import shutil
from typing import List
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from app.core.config import settings
from app.models.solicitacao import Solicitacao
from app.schemas.solicitacao_schema import SolicitationCreate, SolicitationModel
from app.schemas.usuario_schema import UsuarioPayload

class SolicitacaoService:
    from fastapi import Request  # ajuste aqui
# ...

    @staticmethod
    async def listar(
        usuario: UsuarioPayload,
        pagina: int = 1,
        tamanho: int = 10
    ) -> List[SolicitationModel]:
        skip = (pagina - 1) * tamanho

        tipo_usuario: str = usuario.get("tipo")
        usuario_id: str = usuario.get("sub") or usuario.get("_id")

        if tipo_usuario == "empresa":
            filtro = {"empresa_id": usuario_id}
        elif tipo_usuario == "prestador":
            filtro = {"status": "aberta"}
        else:
            raise HTTPException(status_code=403, detail="Acesso negado ao tipo de usuário.")

        documentos = (
            await Solicitacao.find(filtro)
            .sort("-data_criacao")
            .skip(skip)
            .limit(tamanho)
            .to_list()
        )

        solicitacoes = []
        for doc in documentos:
            data = doc.dict(by_alias=True)

            # Substitui nomes de imagens por URLs acessíveis
            imagens = data.get("imagens", [])
            data["imagens"] = [
                f"{settings.BACKEND_URL}/imagens/{nome}" for nome in imagens
            ]

            # Conta interessados únicos
            from app.services.proposta_service import PropostaService
            data["interessados"] = await PropostaService.contar_interessados_unicos(str(doc.id))

            solicitacoes.append(SolicitationModel(**data))

        return solicitacoes

    @staticmethod
    async def obter_por_id(solicitacao_id: str) -> SolicitationModel:
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")

        data = doc.dict(by_alias=True)

        # Se houver imagens, converte nomes para URLs acessíveis
        imagens = data.get("imagens", [])
        data["imagens"] = [
            f"{settings.BACKEND_URL}/imagens/{nome}" for nome in imagens
        ]

        return SolicitationModel(**data)


    @staticmethod
    async def criar(
        dados: SolicitationCreate,
        empresa_id: str,
        arquivos: List[UploadFile] = []
    ) -> SolicitationModel:

        nomes_imagens = []
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        for arquivo in arquivos:
            extensao = os.path.splitext(arquivo.filename)[-1]
            nome_arquivo = f"{uuid4().hex}{extensao}"
            caminho = os.path.join(settings.UPLOAD_DIR, nome_arquivo)

            with open(caminho, "wb") as buffer:
                shutil.copyfileobj(arquivo.file, buffer)

            nomes_imagens.append(nome_arquivo)

        nova = Solicitacao(
            **dados.dict(),
            empresa_id=empresa_id,
            status="aberta",
            interessados=0,
            imagens=nomes_imagens  # ⬅️ salva nomes dos arquivos
        )
        await nova.insert()
        return SolicitationModel(**nova.dict(by_alias=True))

    @staticmethod
    async def atualizar(solicitacao_id: str, atualizacao: SolicitationCreate) -> SolicitationModel:
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        await doc.set(atualizacao.dict())
        return SolicitationModel(**doc.dict(by_alias=True))

    @staticmethod
    async def deletar(solicitacao_id: str):
        doc = await Solicitacao.get(solicitacao_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")
        await doc.delete()
        return {"mensagem": "Solicitação removida com sucesso."}