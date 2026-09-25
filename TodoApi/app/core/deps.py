import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import ALGORITHM, SECRET_KEY
from app.database.connection import get_db_session
from app.models.usuario import UsuarioModel

# Informa ao Swagger e ao FastAPI onde o cliente obtém o token (endpoint /auth/login)
# Isso faz o botão de cadeado do Swagger saber onde enviar usuário e senha
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> UsuarioModel:
    """Valida o token JWT recebido no Header Authorization e retorna o usuário logado."""
    credenciais_invalidas_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. Decodifica e valida assinatura e expiração (exp) automaticamente
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id_str: str | None = payload.get("sub")

        if usuario_id_str is None:
            raise credenciais_invalidas_exception

        usuario_id = int(usuario_id_str)
    except (jwt.PyJWTError, ValueError):
        # Captura erro de token malformado, assinatura adulterada ou expiração vencida
        raise credenciais_invalidas_exception

    # 2. Busca o usuário correspondente no banco
    query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
    resultado = await session.execute(query)
    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise credenciais_invalidas_exception

    return usuario