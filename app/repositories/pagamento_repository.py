from app.models.pagamento import Pagamento

async def salvar_pagamento(dados: dict):
    pagamento = Pagamento(**dados)
    await pagamento.insert()  # <- Beanie cuida do insert no Mongo