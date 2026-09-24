from pydantic import BaseModel, Field

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    preco: float = Field(..., gt=0)
    em_estoque: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: str | None = None
    preco: float | None = Field(None, gt=0)
    em_estoque: bool | None = None

class ProdutoResponse(ProdutoBase):
    id: int