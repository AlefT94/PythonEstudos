from sqlalchemy import Boolean, Float, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class TarefaModel(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    concluida : Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    prioridade : Mapped[int] = mapped_column(Integer,nullable=False,default=1)

    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id"), nullable=False
    )