from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from datetime import datetime
from bson import ObjectId

# Converte ObjectId -> str na serialização
PyObjectId = Annotated[str, BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)]

# ---- INPUT (POST / criação) ----
class PropostaCreate(BaseModel):
    """
    Body para criação de proposta.
    Os IDs (solicitação, prestador, empresa) são derivados do path/token/solicitação.
    """
    mensagem: str = Field(..., max_length=500)

    class Config:
        populate_by_name = True

# ⬇️ NOVO: modelo "slim" do usuário no contexto da proposta
class PropostaUsuarioSlim(BaseModel):
    id: str
    nome: str
    email: EmailStr
    # mantém a chave 'foto' como você está montando no service
    foto: Optional[str] = None

# ---- OUTPUT (responses) ----
class PropostaResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    solicitacao_id: PyObjectId
    prestador_id: PyObjectId
    empresa_id: PyObjectId

    mensagem: str
    data_envio: Optional[datetime] = None
    status: Optional[str] = None
    possui_mensagem_nova: bool = False

    # já suportado no seu service
    prestador_nome: Optional[str] = None

    # ⬇️ NOVO: inclui o bloco 'usuario' retornado pelo service
    usuario: Optional[PropostaUsuarioSlim] = None

    class Config:
        populate_by_name = True

# Compatibilidade com imports antigos
PropostaModel = PropostaResponse