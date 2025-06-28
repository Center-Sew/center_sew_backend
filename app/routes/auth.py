from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.extensions.limiter_extension import limiter
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
    existente = await Usuario.find_one({"email": usuario.email})
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_password(usuario.senha),
        tipo=usuario.tipo,
        documento=usuario.documento,
        localizacao=usuario.localizacao
    )
    await novo_usuario.insert()
    return novo_usuario.model_dump(by_alias=True)

@router.post("/login", response_model=UsuarioAuthResponse)
@limiter.limit("5/minute")
async def login(request: Request, dados: UsuarioLogin):
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
