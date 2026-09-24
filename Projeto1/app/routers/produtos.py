from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services.produto_service import ProdutoService, get_produto_service

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],  # Agrupa no Swagger
)

@router.get("/", response_model=list[ProdutoResponse])
def listar(
    limit: int = 10,
    offset: int = 0,
    service: ProdutoService = Depends(get_produto_service),
) -> list[dict]:
    return service.listar(limit, offset)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
) -> dict:
    produto = service.obter_por_id(produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    return produto

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar(
    dados: ProdutoCreate,
    service: ProdutoService = Depends(get_produto_service),
) -> dict:
    return service.criar(dados)

@router.patch("/{produto_id}", response_model=ProdutoResponse)
def atualizar(
    produto_id: int,
    dados: ProdutoUpdate,
    service: ProdutoService = Depends(get_produto_service),
) -> dict:
    produto = service.atualizar(produto_id, dados)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    return produto

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service),
) -> None:
    removido = service.deletar(produto_id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado."
        )