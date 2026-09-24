from pydantic import BaseModel, Field, ConfigDict

class TarefaBase(BaseModel):
    titulo: str = Field(...,min_length=3,max_length=100 )
    descricao: str | None = None
    concluida: bool = False
    prioridade: int = Field(...,gt=0,le=5)

class TarefaCreate(TarefaBase):
    pass

class TarefaUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    concluida: bool | None = None
    prioridade: int | None = None

class TarefaResponse(TarefaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)