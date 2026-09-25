from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tarefa import TarefaModel
from app.schemas.tarefa import TarefaCreate, TarefaUpdate

class TarefaService():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def listar(self, limit: int = 10, offset: int = 0, apenas_pendentes: bool = False) -> list[TarefaModel]:
        query = select(TarefaModel)

        if apenas_pendentes:
            query = query.where(TarefaModel.concluida == False)

        query = query.offset(offset).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def obter_por_id(self, tarefa_id: int) -> TarefaModel|None:
        query = select(TarefaModel).where(TarefaModel.id == tarefa_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def criar(self, dado: TarefaCreate) -> TarefaModel:
        nova_tarefa = TarefaModel(**dado.model_dump())
        self.session.add(nova_tarefa)
        await self.session.commit()

        # Faz o refresh para obter o id gerado pelo autoincrement do banco
        await self.session.refresh(nova_tarefa)
        return nova_tarefa
    
    async def atualizar(self, tarefa_id: int, dados: TarefaUpdate) -> TarefaModel | None:
        tarefa = await self.obter_por_id(tarefa_id)

        if tarefa is None:
            return None

        alteracoes = dados.model_dump(exclude_unset=True)

        for campo, valor in alteracoes.items():
            setattr(tarefa,campo,valor)

        await self.session.commit()
        await self.session.refresh(tarefa)
        return tarefa

    async def deletar(self,tarefa_id: int) -> bool:
        tarefa = await self.obter_por_id(tarefa_id)

        if tarefa is None:
            return False

        await self.session.delete(tarefa)
        await self.session.commit()
        return True        