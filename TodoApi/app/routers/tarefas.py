from collections.abc import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import obter_usuario_atual
from app.database.connection import get_db_session
from app.models.usuario import UsuarioModel
from app.services.tarefa_service import TarefaService
from app.schemas.tarefa import TarefaResponse, TarefaUpdate, TarefaCreate
from app.models.tarefa import TarefaModel

router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"],
)

def get_service(session: AsyncSession = Depends(get_db_session)) -> TarefaService:
    """Fábrica do serviço recebendo a sessão scoped aberta para a requisição."""
    return TarefaService(session=session)

@router.get("/", response_model=list[TarefaResponse])
async def listar(limit: int = 10, offset: int = 0, apenas_pendentes: bool = False, service: TarefaService = Depends(get_service), usuario_atual: UsuarioModel = Depends(obter_usuario_atual)) -> list[TarefaModel]:
    return await service.listar(limit=limit, offset=offset, apenas_pendentes=apenas_pendentes)

@router.post("/", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    dado: TarefaCreate,
    service: TarefaService = Depends(get_service),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual),
) -> TarefaModel:
    return await service.criar(dado, usuario_id=usuario_atual.id)


@router.put("/{tarefa_id}", response_model=TarefaResponse)
async def atualizar(
    tarefa_id: int,
    dados: TarefaUpdate,
    service: TarefaService = Depends(get_service),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual),
) -> TarefaModel:
    tarefa = await service.atualizar(tarefa_id, dados, usuario_id=usuario_atual.id)
    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada.",
        )
    return tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(
    tarefa_id: int,
    service: TarefaService = Depends(get_service),
    usuario_atual: UsuarioModel = Depends(obter_usuario_atual),
) -> None:
    sucesso = await service.deletar(tarefa_id, usuario_id=usuario_atual.id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada.",)