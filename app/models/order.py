from tkinter import CASCADE

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from enum import Enum as PyEnum
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship




class StatusEnum(str,PyEnum):
    PENDING = "pendiente"
    APROVED = "aprobado"
    REJECTED = "rechazado"

class OrderBatch(Base):
    __tablename__ = "order_batches"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_by :Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default= func.now())

    user :Mapped["User"] = relationship( back_populates="batches") # type: ignore
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="batch",cascade="all, delete-orphan", passive_deletes=True)

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    batch_id :Mapped[int] = mapped_column(ForeignKey("order_batches.id", ondelete=CASCADE), nullable=False,)

    fecha: Mapped[DateTime] = mapped_column(DateTime)
    id_profesional: Mapped[str|None] = mapped_column(String(100))
    profesional : Mapped[str|None] = mapped_column(String(255))
    no_orden: Mapped[str|None] = mapped_column(String(100))
    codigo: Mapped[str|None] = mapped_column(String(100))
    procedimiento: Mapped[str|None] = mapped_column(String(500))
    cantidad: Mapped[int|None] = mapped_column(Integer)
    dosis: Mapped[str|None] = mapped_column(String(100))
    dias_tto: Mapped[int|None] = mapped_column(Integer)

    status : Mapped[StatusEnum] = mapped_column(Enum(StatusEnum,name="order_status_enum"), default=StatusEnum.PENDING)
    error_message: Mapped[str|None] = mapped_column(Text)

    batch: Mapped["OrderBatch"] = relationship("OrderBatch",back_populates="orders")
