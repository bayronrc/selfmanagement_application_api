from datetime import date
import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime,Enum,  ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class RipsOldStatus(str,PyEnum):
    REVISADO =  "revisado"
    PENDIENTE  = "pendiente"
    AUDITADO = "auditado"

class RipsOld(Base):
    __tablename__ = "rips_old"
    user_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    uploaded_by :Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[RipsOldStatus] = mapped_column(Enum(RipsOldStatus,name="rips_status"), default=RipsOldStatus.PENDIENTE, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now() )
