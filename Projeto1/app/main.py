from fastapi import FastAPI
from app.routers import produtos

app = FastAPI(
    title="Catálogo de Produtos - Arquitetura em Camadas",
    version="2.0.0",
)

# Registra o Router (como registrar Controllers no ASP.NET)
app.include_router(produtos.router)

@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}