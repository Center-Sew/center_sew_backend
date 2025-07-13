from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.extensions.limiter_extension import limiter
from app.models.empresa import Empresa
from app.models.prestador import Prestador
from app.models.usuario import Usuario
from app.auth.auth_handler import hash_password, verify_password, create_access_token
from app.schemas.usuario_schema import (  # <- AJUSTE AQUI
    UsuarioAuthResponse,
    UsuarioCreate,
    UsuarioLogin,
    UsuarioPayload,
    UsuarioResponse,
)

router = APIRouter(tags=["Autenticação"])

@router.post("/register", response_model=UsuarioResponse)
async def register(usuario: UsuarioCreate):
    print(usuario.email)
    if await Usuario.find_one({"email": usuario.email}):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # 1 ─ cria o usuário-base
    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_password(usuario.senha),
        tipo=usuario.tipo,                         # "prestador" | "empresa"
        documento=usuario.documento,
        localizacao=usuario.localizacao,
    )
    await novo.insert()

    # 2 ─ cria o perfil especializado
    if usuario.tipo == "prestador":
        if not usuario.tipo_fiscal or not usuario.especialidades:
            raise HTTPException(422, "Campos tipo_fiscal e especialidades são obrigatórios p/ prestador.")
        await Prestador(
            usuario=novo,
            tipo_fiscal=usuario.tipo_fiscal,
            especialidades=usuario.especialidades,
            localizacao=usuario.localizacao,
            descricao_portfolio=usuario.descricao_portfolio,
        ).insert()

    elif usuario.tipo == "empresa":
        if not usuario.razaosocial:
            raise HTTPException(422, "Campo razaosocial é obrigatório p/ empresa.")
        await Empresa(
            usuario=novo,
            razaosocial=usuario.razaosocial,
            cnpj=usuario.documento,
            segmento=usuario.segmento,
            localizacao=usuario.localizacao,
        ).insert()

    return UsuarioResponse(**novo.dict(by_alias=True))

@router.post("/login", response_model=UsuarioAuthResponse)
@limiter.limit("5/minute")
async def login(request: Request, dados: UsuarioLogin):
    print("Chegou aqui")
    usuario = await Usuario.find_one(Usuario.email == dados.email)
    if not usuario or not verify_password(dados.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos."
        )

    token = create_access_token({
        "sub": str(usuario.id),
        "tipo": usuario.tipo  # 🔐 importante!
    })

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
