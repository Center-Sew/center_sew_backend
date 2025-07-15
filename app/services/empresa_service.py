from typing import Optional
from bson import ObjectId

from app.models.empresa import Empresa
from app.schemas.empresa_schema import EmpresaSlim


async def carregar_empresa_slim(empresa_id: str) -> Optional[EmpresaSlim]:
    try:
        empresa = await Empresa.get(ObjectId(empresa_id))
        if empresa is None:
            return None

        return EmpresaSlim(
            id=str(empresa.id),
            razao_social=empresa.razao_social,
            nome_fantasia=empresa.nome_fantasia,
            email=empresa.email,
            telefone=empresa.telefone,
            endereco=empresa.localizacao.get("endereco"),
            cidade=empresa.localizacao.get("cidade"),
            estado=empresa.localizacao.get("estado"),
            bairro=empresa.localizacao.get("bairro"),
            foto=empresa.foto,
        )

    except Exception as e:
        # 🔒 Log ou tratamento adicional se desejar
        return None