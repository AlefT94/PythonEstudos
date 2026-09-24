from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    # Mapped[...] é o sistema moderno do SQLAlchemy 2.0 com tipagem estrita
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    em_estoque: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)