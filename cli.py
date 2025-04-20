from seeds.servico_seed import seed_servicos
from seeds.solicitacao_seed import seed_solicitacoes
from seeds.usuario_seed import seed_usuarios
import typer
import asyncio
from typing import List

from app.database.mongo import init_mongo

# Registro de funções de seed
# from app.seeds.usuario_seed import seed_usuarios
# from app.seeds.solicitacao_seed import seed_solicitacoes

app = typer.Typer()

SEED_MAP = {
    "usuarios": seed_usuarios,
    "servicos": seed_servicos,
    "solicitacoes": seed_solicitacoes
}

@app.command()
def seed(modulos: List[str] = typer.Argument(None, help="Módulos para popular (ex: servicos, usuarios)")):
    """Executa seeds de dados para os módulos indicados."""
    async def run():
        await init_mongo()

        if not modulos:
            typer.echo("ℹ️  Nenhum módulo informado. Use por exemplo: `python cli.py seed usuarios solicitacoes`")
            typer.echo(f"📦 Módulos disponíveis: {', '.join(SEED_MAP.keys())}")
            return

        # Sempre executa seed de usuários antes de outros que dependem
        if "usuarios" in modulos:
            await SEED_MAP["usuarios"]()
            typer.echo("✅ Seed de 'usuarios' concluído.")

        for modulo in modulos:
            if modulo == "usuarios":
                continue  # Já executado
            seed_func = SEED_MAP.get(modulo)
            if seed_func:
                await seed_func()
                typer.echo(f"✅ Seed de '{modulo}' concluído.")
            else:
                typer.echo(f"⚠️  Módulo desconhecido: {modulo}")

    asyncio.run(run())

if __name__ == "__main__":
    app()
