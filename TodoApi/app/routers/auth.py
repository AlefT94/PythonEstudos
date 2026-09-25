from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db_session
from app.schemas.usuario import TokenResponse, UsuarioCreate, UsuarioResponse
from app.services.auth_service import AuthService
from app.core.deps import obter_usuario_atual
from app.models.usuario import UsuarioModel

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


def get_auth_service(session: AsyncSession = Depends(get_db_session)) -> AuthService:
    """Fábrica do AuthService com injeção da sessão do banco."""
    return AuthService(session=session)


@router.post(
    "/registrar",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrar(
    dados: UsuarioCreate,
    service: AuthService = Depends(get_auth_service),
) -> UsuarioResponse:
    usuario = await service.registrar(dados)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário cadastrado com este e-mail.",
        )
    return usuario


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    # O OAuth2PasswordRequestForm padroniza os campos como 'username' e 'password'
    # No nosso sistema, o 'username' enviado será o próprio e-mail do usuário
    token = await service.autenticar(email=form_data.username, senha=form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me", response_model=UsuarioResponse)
async def ler_usuario_logado(
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual),
) -> UsuarioModel:
    """Retorna os dados do usuário atualmente autenticado via JWT."""
    return usuario_atual