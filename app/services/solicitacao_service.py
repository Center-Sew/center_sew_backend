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
from app.services.proposta_service import PropostaService


class SolicitacaoService:

    @staticmethod
    async def listar(usuario: dict, pagina: int = 1, tamanho: int = 10) -> List[SolicitationModel]:
        skip = (pagina - 1) * tamanho

        filtro = {}

        if usuario["tipo"] == "empresa":
            # Empresa visualiza as próprias solicitações
            filtro = {"usuario_id": ObjectId(usuario["sub"]),
                "proposta_aceita": False}
        elif usuario["tipo"] == "prestador":
            # Prestador visualiza solicitações abertas, compatíveis com seu tipo_fiscal
            usuario_model = await Usuario.get(ObjectId(usuario["sub"]))

            if not usuario_model or not usuario_model.tipo_fiscal:
                return []  # Sem tipo fiscal definido, não pode ver nada

            # Solicitações abertas onde o tipo_fiscal desejado possui interseção com o do usuário
            filtro = {
                "status": "aberta",
                "perfil_desejado.tipo_fiscal": {
                    "$in": usuario_model.tipo_fiscal
                },
                "proposta_aceita": False
            }
        else:
            # Outros tipos de usuário não visualizam nada
            return []

        docs = (
            await Solicitacao.find(filtro)
            .sort("-data_criacao")
            .skip(skip)
            .limit(tamanho)
            .to_list()
        )

        solicitacoes: List[SolicitationModel] = []

        for doc in docs:
            try:
                autor = await Usuario.get(doc.usuario_id)
            except Exception as e:
                print(f"[!] Erro ao buscar autor: {e}")
                continue

            if not autor:
                print(f"[!] Autor não encontrado para usuario_id: {doc.usuario_id}")
                continue

            data = doc.model_dump()
            data["usuario_id"] = str(doc.usuario_id)
            data["usuario"] = {
                "id": str(autor.id),
                "nome": autor.nome,
                "email": autor.email,
                "segmento": autor.segmento,
                "localizacao": autor.localizacao.dict(),
                "foto": f"{settings.BACKEND_URL}/imagens/perfil/{autor.foto}" if autor.foto else None,
            }
            data["imagens"] = [f"{settings.BACKEND_URL}/imagens/solicitacoes/{n}" for n in doc.imagens or []]
            data["interessados"] = await PropostaService.contar_interessados_unicos(str(doc.id))
            
            print("Interessados: ", data)
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
        # Verifica se o usuário existe
        autor = await Usuario.get(ObjectId(usuario_id))
        if not autor:
            print("Não existe: ", usuario_id)
            raise HTTPException(status_code=404, detail="Usuário (empresa) não encontrado")

        # Salva imagens
        nomes = []
        pasta_destino = os.path.join(settings.UPLOAD_DIR, "imagens", "solicitacoes")
        os.makedirs(pasta_destino, exist_ok=True)

        for arq in arquivos:
            ext = os.path.splitext(arq.filename)[-1]
            nome = f"{uuid4().hex}{ext}"
            caminho_arquivo = os.path.join(pasta_destino, nome)

            with open(caminho_arquivo, "wb") as buf:
                shutil.copyfileobj(arq.file, buf)

            nomes.append(nome)

        # Cria nova solicitação
        nova = Solicitacao(
            **dados.model_dump(),
            usuario_id=ObjectId(usuario_id),
            status="aberta",
            interessados=0,
            imagens=nomes
        )
        await nova.insert()

        # Retorna com os dados do autor
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

    
    @staticmethod
    async def deletar(solicitacao_id: str, usuario_id: str):
        doc = await Solicitacao.get(solicitacao_id)
        
        if not doc:
            raise HTTPException(404, "Solicitação não encontrada.")

        # Verifica se quem está deletando é o dono
        if str(doc.usuario_id) != usuario_id:
            raise HTTPException(403, "Acesso negado. Você não é dono desta solicitação.")

        # Deleta imagens (se existirem)
        for imagem_nome in doc.imagens or []:
            caminho = os.path.join(settings.UPLOAD_DIR, "imagens", "solicitacoes", imagem_nome)
            if os.path.exists(caminho):
                os.remove(caminho)

        await doc.delete()
        return {"detail": "Solicitação cancelada com sucesso."}