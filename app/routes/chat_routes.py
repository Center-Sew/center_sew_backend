from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.chat_schema import MensagemCreate, MensagemResponse
from app.services.chat_service import ChatService
from app.auth.auth_bearer import JWTBearer
from app.security.rbac import role_required

router = APIRouter(prefix="/chat", tags=["Chat"])

# ✅ Enviar mensagem (empresa ou prestador, por proposta ou serviço)
@router.post("/mensagem", response_model=MensagemResponse)
async def enviar_mensagem(
    mensagem: MensagemCreate,
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    if not mensagem.proposta_id and not mensagem.servico_id:
        raise HTTPException(status_code=400, detail="proposta_id ou servico_id é obrigatório")

    resultado = await ChatService.enviar_mensagem(
        proposta_id=mensagem.proposta_id,
        servico_id=mensagem.servico_id,
        remetente_id=token_payload["sub"],
        destinatario_id=mensagem.destinatario_id,
        texto=mensagem.texto
    )
    return MensagemResponse(**resultado.model_dump(by_alias=True))

def _as_object_id(value: str, field: str) -> ObjectId:
    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=400, detail=f"{field} inválido")


@router.get("/mensagens", response_model=List[MensagemResponse])
async def listar_mensagens(
    proposta_id: Optional[str] = Query(None),
    servico_id: Optional[str]  = Query(None),
    empresa_id: str = Query(...),
    prestador_id: str = Query(...),
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    # 1) XOR entre proposta_id e servico_id
    if not ((proposta_id is not None) ^ (servico_id is not None)):
        raise HTTPException(status_code=400, detail="Informe exatamente uma origem: proposta_id OU servico_id")

    empresa_oid   = _as_object_id(empresa_id, "empresa_id")
    prestador_oid = _as_object_id(prestador_id, "prestador_id")

    # 2) O usuário autenticado precisa ser um dos participantes informados
    aut_id  = ObjectId(token_payload["sub"])  # id do usuário logado
    aut_role = token_payload.get("role")
    if aut_role == "empresa" and aut_id != empresa_oid:
        raise HTTPException(status_code=403, detail="Token não corresponde à empresa informada")
    if aut_role == "prestador" and aut_id != prestador_oid:
        raise HTTPException(status_code=403, detail="Token não corresponde ao prestador informado")

    # 3) Delegar para o service com verificação de pertencimento
    if proposta_id:
        origem = "proposta"
        origem_oid = _as_object_id(proposta_id, "proposta_id")
    else:
        origem = "servico"
        origem_oid = _as_object_id(servico_id, "servico_id")

    mensagens = await ChatService.listar_mensagens(
        origem=origem, 
        origem_id=origem_oid, 
        empresa_id=empresa_oid, 
        prestador_id=prestador_oid
    )

    # 4) Retorno já no formato esperado pelo frontend
    return [MensagemResponse(**m.model_dump(by_alias=True)) for m in mensagens]


# ✅ Marcar mensagens como lidas (por proposta ou serviço)
@router.put("/mensagens/lidas/{id}")
async def marcar_mensagens_como_lidas(
    id: str,
    tipo: str = Query(..., description="proposta ou servico"),
    token_payload: dict = Depends(role_required(["empresa", "prestador"]))
):
    if tipo == "proposta":
        await ChatService.marcar_como_lidas(proposta_id=id, usuario_id=token_payload["sub"])
    elif tipo == "servico":
        await ChatService.marcar_como_lidas(servico_id=id, usuario_id=token_payload["sub"])
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido. Use 'proposta' ou 'servico'.")

    return {"status": "ok"}
