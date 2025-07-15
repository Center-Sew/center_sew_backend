from fastapi import APIRouter, HTTPException, status, Request
from app.extensions.limiter_extension import limiter
from app.models.usuario import Usuario
from app.core.security import hash_password, verify_password, create_access_token     # << caminho que já usa hash/senha
from app.schemas.usuario_schema import (
    UsuarioAuthResponse,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioPayload,
    UsuarioResponse,
)

router = APIRouter(tags=["Autenticação"])

@router.post("/register", response_model=UsuarioResponse)
async def register(usuario: UsuarioCreate):
    if await Usuario.find_one({"email": usuario.email.lower()}):
        raise HTTPException(400, "E‑mail já cadastrado.")

    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email.lower(),
        senha=hash_password(usuario.senha),
        tipo=usuario.tipo,                      # "empresa" | "prestador" | "fornecedor"
        documento=usuario.documento,
        telefone=usuario.telefone,
        localizacao=usuario.localizacao,
        foto=usuario.foto,
        razaosocial=usuario.razaosocial,
        segmento=usuario.segmento,
        tipo_fiscal=usuario.tipo_fiscal,
        especialidades=usuario.especialidades,
        descricao_portfolio=usuario.descricao_portfolio,
        disponivel=True,
    )
    await novo.insert()

    return UsuarioResponse(**novo.model_dump(by_alias=True))


@router.post("/login", response_model=UsuarioAuthResponse)
@limiter.limit("5/minute")
async def login(request: Request, dados: UsuarioLogin):
    usuario = await Usuario.find_one(Usuario.email == dados.email.lower())
    if not usuario or not verify_password(dados.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="E‑mail ou senha inválidos.")

    token = create_access_token({"sub": str(usuario.id), "tipo": usuario.tipo})

    return UsuarioAuthResponse(
        access_token=token,
        user=UsuarioPayload(
            id=str(usuario.id),
            nome=usuario.nome,
            email=usuario.email,
            tipo=usuario.tipo,
            documento=usuario.documento,
            localizacao=usuario.localizacao
        )
    )