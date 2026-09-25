from collections.abc import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db_session
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
async def listar(limit: int = 10, offset: int = 0, apenas_pendentes: bool = False, service: TarefaService = Depends(get_service)) -> list[TarefaModel]:
    return await service.listar(limit=limit, offset=offset, apenas_pendentes=apenas_pendentes)

@router.post("/", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
async def criar(dados: TarefaCreate,
                service: TarefaService = Depends(get_service)) -> TarefaResponse:
    return await service.criar(dados)