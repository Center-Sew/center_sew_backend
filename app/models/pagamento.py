from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional, Dict

class Pagamento(Document):
    id_pagamento: int = Field(..., description="ID do pagamento no Mercado Pago")
    status: str = Field(..., description="Status atual do pagamento (e.g. approved, rejected)")
    status_detail: Optional[str] = Field(None, description="Detalhe do status (e.g. cc_rejected_high_risk)")
    descricao: str = Field(..., description="Descrição do item comprado")
    valor: float = Field(..., description="Valor do pagamento")
    metodo_pagamento: Optional[str] = Field(None, description="Forma de pagamento (e.g. credit_card)")
    tipo_pagamento: Optional[str] = Field(None, description="Tipo do método (e.g. credit_card, ticket)")
    data_criacao: datetime = Field(default_factory=datetime.utcnow)

    user_id: str = Field(..., description="ID do usuário no sistema")
    tipo_usuario: str = Field(..., description="Tipo do usuário: empresa ou prestador")
    plano_id: str = Field(..., description="ID do plano no sistema")
    plano_nome: str = Field(..., description="Nome do plano")
    plano_valor: float = Field(..., description="Valor do plano")

    payload_completo: Optional[Dict] = Field(None, description="Payload completo do Mercado Pago para referência")

    class Settings:
        name = "pagamentos"