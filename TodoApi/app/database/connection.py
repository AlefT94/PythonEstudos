from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# String de conexão usando o driver assíncrono asyncpg
# Formato: postgresql+driver://usuario:senha@host:porta/nome_banco
DATABASE_URL = "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/todo_db"

# Engine: O pool de conexões (equivalente à configuração de Connection Pooling do EF Core)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Imprime no console as queries SQL geradas (ótimo para estudos)
)

# Fábrica de sessões (cria a instância de trabalho, semelhante ao DbContext)
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Classe Base para os modelos ORM (onde ficam mapeadas as tabelas)
class Base(DeclarativeBase):
    pass

# Dependency Injection para o FastAPI (Ciclo de vida Scoped por requisição)
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session