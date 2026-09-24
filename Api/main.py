from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Minha Primeira API em Python",
    version="1.0.0",
)

# 1. DTO / ViewModel (Pydantic Model)
# Valida tipagem em tempo de execução e serializa/deserializa JSON
class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50, example="Teclado Mecânico")
    preco: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    em_estoque: bool = True

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    em_estoque: bool

class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=50)
    preco: float | None = Field(None, gt=0)
    em_estoque: bool | None = None

# "Banco em memória" para teste rápido
banco_produtos: dict[int, dict] = {}
contador_id = 0

# 2. Endpoints
@app.get("/")
def home() -> dict[str, str]:
    return {"status": "ok", "mensagem": "API rodando!"}

@app.post(
    "/produtos", 
    response_model=ProdutoResponse, 
    status_code=status.HTTP_201_CREATED
)
def criar_produto(dados: ProdutoCreate) -> dict:
    global contador_id
    contador_id += 1
    
    # .model_dump() converte o schema Pydantic em um dict nativo do Python
    novo_produto = {"id": contador_id, **dados.model_dump()}
    banco_produtos[contador_id] = novo_produto
    return novo_produto

@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(limit: int = 10, offset: int = 0) -> list[dict]:
    # Query parameters são inferidos automaticamente se não estiverem no path!
    todos = list(banco_produtos.values())
    return todos[offset : offset + limit]

@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int) -> dict:
    produto = banco_produtos.get(produto_id)
    if not produto:
        # Equivalente ao NotFound() do ASP.NET Core
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    return produto

@app.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(dado: ProdutoUpdate, produto_id: int) -> dict:
    produto = banco_produtos.get(produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = dado.model_dump(exclude_unset=True)
    produto.update(update_data)
    return produto

@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int) -> None:
    produto = banco_produtos.get(produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Produto com ID {produto_id} não encontrado."
        )

    del banco_produtos[produto_id]