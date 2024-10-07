from datetime import datetime
from sqlalchemy import Numeric, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    # created_at: Mapped[datetime] = mapped_column(
    #     index=True,
    #     server_default=func.now()
    # )
    # updated_at: Mapped[datetime] = mapped_column(
    #     index=True,
    #     server_default=func.now(),
    #     onupdate=func.now()
    # )
    __table_args__ = {'extend_existing': True}


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(30), nullable=False)
    telegram_id : Mapped[int]


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


class Banner(Base):
    __tablename__ = 'banner'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone_number: Mapped[int] = mapped_column(BigInteger, nullable=False)


class Material(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    photo:Mapped[str] = mapped_column(String(150), nullable=False)
    packing: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    category: Mapped['Category'] = relationship(backref='products')


class Note(Base):
    __tablename__ = "notes"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(50), nullable=False)
    description : Mapped[str] = mapped_column(Text, nullable=False)
    photo : Mapped[str] = mapped_column(String(150), nullable=True)
