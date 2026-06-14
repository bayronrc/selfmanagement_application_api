from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func

from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship




class StatusEnum(str,Enum):
    PENDING = "pendiente"
    APROVED = "aprobado"
    REJECTED = "rechazado"

class OrderBatch(Base):
    __tablename__ = "order_batches"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    uploaded_by :Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default= func.now())

    user :Mapped["User"] = relationship( back_populates="batches") # type: ignore
    orders: Mapped[list["Order"]] = relationship( back_populates="batch")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    batch_id :Mapped[int] = mapped_column(ForeignKey("orders_batches.id"), nullable=False)

    fecha: Mapped[DateTime] = mapped_column(String(20))
    id_profesional: Mapped[str|None] = mapped_column(String(100))
    profesional : Mapped[str|None] = mapped_column(String(255))
    no_orden: Mapped[str|None] = mapped_column(String(100))
    codigo: Mapped[str|None] = mapped_column(String(100))
    procedimiento: Mapped[str|None] = mapped_column(String(500))
    cantidad: Mapped[int|None] = mapped_column(Integer)
    dosis: Mapped[str|None] = mapped_column(String(100))
    dias_tto: Mapped[int|None] = mapped_column(Integer)

    status : Mapped[str] = mapped_column(String(20), default=StatusEnum.PENDING)
    error_message: Mapped[str|None] = mapped_column(Text)

    batch: Mapped["OrderBatch"] = relationship( back_populates="orders")
