from collections.abc import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db_session
from app.models.produto import ProdutoModel
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services.produto_service import ProdutoService

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)

def get_service(session: AsyncSession = Depends(get_db_session)) -> ProdutoService:
    """Fábrica do serviço recebendo a sessão scoped aberta para a requisição."""
    return ProdutoService(session=session)

@router.get("/", response_model=list[ProdutoResponse])
async def listar(
    limit: int = 10,
    offset: int = 0,
    service: ProdutoService = Depends(get_service),
) -> Sequence[ProdutoModel]:
    return await service.listar(limit=limit, offset=offset)

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def obter(
    produto_id: int,
    service: ProdutoService = Depends(get_service),
) -> ProdutoModel:
    produto = await service.obter_por_id(produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado.",
        )
    return produto

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    dados: ProdutoCreate,
    service: ProdutoService = Depends(get_service),
) -> ProdutoModel:
    return await service.criar(dados)

@router.patch("/{produto_id}", response_model=ProdutoResponse)
async def atualizar(
    produto_id: int,
    dados: ProdutoUpdate,
    service: ProdutoService = Depends(get_service),
) -> ProdutoModel:
    produto = await service.atualizar(produto_id, dados)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado.",
        )
    return produto

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(
    produto_id: int,
    service: ProdutoService = Depends(get_service),
) -> None:
    sucesso = await service.deletar(produto_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado.",
        )