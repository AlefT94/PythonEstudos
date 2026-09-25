from fastapi import FastAPI
from app.routers import tarefas, auth

app = FastAPI(
    title="Lista de Tarefas - Arquitetura em Camadas",
    version="2.0.0",
)

# Registra o Router (como registrar Controllers no ASP.NET)
app.include_router(auth.router)
app.include_router(tarefas.router)

@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}