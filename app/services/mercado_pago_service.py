import httpx
import logging

ACCESS_TOKEN = "APP_USR-221678601026584-052909-755b97feb1c1fef7bf5fb5ef72b98920-2465054530"

async def buscar_detalhes_pagamento(payment_id: str) -> dict:
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Erro na chamada Mercado Pago: {e}")
        return {}