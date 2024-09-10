from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        index=True,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        index=True,
        server_default=func.now(),
        onupdate=func.now()
    )


class Users(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(30), nullable=False)
    telegram_id : Mapped[int]
