from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import criar_token_acesso, gerar_hash_senha, verificar_senha
from app.models.usuario import UsuarioModel
from app.schemas.usuario import UsuarioCreate


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obter_por_email(self, email: str) -> UsuarioModel | None:
        """Busca um usuário no banco a partir do seu endereço de e-mail."""
        query = select(UsuarioModel).where(UsuarioModel.email == email)
        resultado = await self.session.execute(query)
        return resultado.scalar_one_or_none()

    async def registrar(self, dados: UsuarioCreate) -> UsuarioModel | None:
        """Cadastra um novo usuário no banco com a senha hasheada.

        Retorna None se o e-mail já estiver em uso.
        """
        usuario_existente = await self.obter_por_email(dados.email)
        if usuario_existente:
            return None

        novo_usuario = UsuarioModel(
            email=dados.email,
            senha_hash=gerar_hash_senha(dados.senha),
        )

        self.session.add(novo_usuario)
        await self.session.commit()
        await self.session.refresh(novo_usuario)
        return novo_usuario

    async def autenticar(self, email: str, senha: str) -> str | None:
        """Valida as credenciais. Se válidas, retorna o token JWT assinado; senão, None."""
        usuario = await self.obter_por_email(email)
        if not usuario:
            return None

        # Valida a senha plana com o hash seguro do banco
        if not verificar_senha(senha, usuario.senha_hash):
            return None

        # Cria o payload com o "sub" (subject), que por convenção da RFC 7519 identifica o usuário
        payload_token = {"sub": str(usuario.id), "email": usuario.email}
        token = criar_token_acesso(dados=payload_token)
        return token