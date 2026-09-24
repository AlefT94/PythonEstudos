from app.schemas.produto import ProdutoCreate, ProdutoUpdate

class ProdutoService:
    def __init__(self) -> None:
        # Simulando um repositório / tabela
        self._banco: dict[int, dict] = {}
        self._contador_id: int = 0

    def listar(self, limit: int = 10, offset: int = 0) -> list[dict]:
        todos = list(self._banco.values())
        return todos[offset : offset + limit]

    def obter_por_id(self, produto_id: int) -> dict | None:
        return self._banco.get(produto_id)

    def criar(self, dados: ProdutoCreate) -> dict:
        self._contador_id += 1
        novo = {"id": self._contador_id, **dados.model_dump()}
        self._banco[self._contador_id] = novo
        return novo

    def atualizar(self, produto_id: int, dados: ProdutoUpdate) -> dict | None:
        produto = self.obter_por_id(produto_id)
        if produto is None:
            return None
        
        alteracoes = dados.model_dump(exclude_unset=True)
        produto.update(alteracoes)
        return produto

    def deletar(self, produto_id: int) -> bool:
        if produto_id in self._banco:
            del self._banco[produto_id]
            return True
        return False

# Instância única para simular um serviço Singleton/Scoped na memória
_instancia_singleton = ProdutoService()

def get_produto_service() -> ProdutoService:
    """Função de fábrica usada pela Injeção de Dependências."""
    return _instancia_singleton