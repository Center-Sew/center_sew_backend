import json
from pathlib import Path
from app.enums.tipo_fiscal import TipoFiscal
from app.enums.tipo_servico import TipoServico
from app.models.solicitacao import Solicitacao
from app.models.perfil_desejado import PerfilDesejado
from app.models.localizacao import Localizacao
from app.models.usuario import Usuario

async def seed_solicitacoes():
    await Solicitacao.find_all().delete()

    # Pega todos os usuários do tipo empresa para serem "empresa_id"
    empresas = await Usuario.find(Usuario.tipo == "empresa").to_list()
    prestadores = await Usuario.find(Usuario.tipo == "prestador").to_list()

    if not empresas:
        raise Exception("Nenhuma empresa encontrada para gerar solicitações.")
    if len(prestadores) < 2:
        raise Exception("Cadastre ao menos dois prestadores para gerar interessados.")

    empresa = empresas[0]  # Usar a primeira empresa cadastrada
    interessados = [str(p.id) for p in prestadores[:2]]

    path = Path(__file__).parent / "data" / "solicitacoes.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Gerar 4 solicitações usando os dados do JSON como base
    for i in range(4):
        base = data[0] if i == 0 else {
            "titulo": f"Solicitação {i+1}",
            "subtitulo": f"Descrição curta {i+1}",
            "descricao": f"Descrição detalhada da solicitação número {i+1}.",
            "perfil_desejado": {
                "tipo_fiscal": ["CNPJ"] if i % 2 == 0 else ["CPF"],
                "tipo_servico": "Costura de cortina" if i % 2 == 0 else "Bainha de calça",
                "descricao": f"Serviço especializado {i+1}",
                "localizacao_alvo": {
                    "cidade": "Campinas" if i % 2 == 0 else "São Paulo",
                    "estado": "SP",
                    "bairro": "Centro",
                    "tipo": "cidade",
                    "valor": "Campinas" if i % 2 == 0 else "São Paulo"
                }
            }
        }

        perfil_desejado = PerfilDesejado(
            tipo_fiscal=[TipoFiscal(f.upper()) for f in base["perfil_desejado"]["tipo_fiscal"]],
            tipo_servico=TipoServico(base["perfil_desejado"]["tipo_servico"]),
            descricao=base["perfil_desejado"]["descricao"],
            localizacao_alvo=Localizacao(
                **base["perfil_desejado"]["localizacao_alvo"]
            )
        )

        solicitacao = Solicitacao(
            titulo=base["titulo"],
            subtitulo=base["subtitulo"],
            descricao=base["descricao"],
            empresa_id=str(empresa.id),
            perfil_desejado=perfil_desejado,
            interessados=interessados,
            status="aberta"
        )
        await solicitacao.insert()

    print("✅ Seed de solicitações gerada com 4 registros.")