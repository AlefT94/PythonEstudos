from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.produto import ProdutoModel
from app.schemas.produto import ProdutoCreate, ProdutoUpdate

class ProdutoService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def listar(self, limit: int = 10, offset: int = 0) -> list[ProdutoModel]:
        query = select(ProdutoModel).offset(offset).limit(limit)
        result = await self.session.execute(query)
        # .scalars().all() extrai os objetos ProdutoModel da tupla de resultados
        return list(result.scalars().all())

    async def obter_por_id(self, produto_id: int) -> ProdutoModel | None:
        query = select(ProdutoModel).where(ProdutoModel.id == produto_id)
        result = await self.session.execute(query)
        # scalar_one_or_none() equivale ao FirstOrDefaultAsync() do EF Core
        return result.scalar_one_or_none()

    async def criar(self, dados: ProdutoCreate) -> ProdutoModel:
        # Cria a instância do Model ORM a partir do schema validado
        novo_produto = ProdutoModel(**dados.model_dump())
        self.session.add(novo_produto)
        await self.session.commit()
        # Faz o refresh para obter o id gerado pelo autoincrement do banco
        await self.session.refresh(novo_produto)
        return novo_produto

    async def atualizar(self, produto_id: int, dados: ProdutoUpdate) -> ProdutoModel | None:
        produto = await self.obter_por_id(produto_id)
        if produto is None:
            return None

        # Pega apenas os campos enviados pelo cliente
        alteracoes = dados.model_dump(exclude_unset=True)
        for campo, valor in alteracoes.items():
            setattr(produto, campo, valor)

        await self.session.commit()
        await self.session.refresh(produto)
        return produto

    async def deletar(self, produto_id: int) -> bool:
        produto = await self.obter_por_id(produto_id)
        if produto is None:
            return False

        await self.session.delete(produto)
        await self.session.commit()
        return True