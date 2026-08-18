from datetime import date
import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime,Enum,  ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

class Rips(Base):
    __table__:str = "rips"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    factura : Mapped[str] = mapped_column(String(20),comment="Numeor de factura")
    codigo_habilitacion: Mapped[str] = mapped_column(String(20), comment="codigo habilitacion prestador")
    tipo_nota: Mapped[str] = mapped_column(String(2), nullable=True, comment="tipo nota")
    num_nota: Mapped[str] = mapped_column(String(20), nullable=True, comment="numero de nota")

    usuarios: Mapped[list["RipsUsuarios"]] = relationship(
        back_populates="rips",
        cascade="all, delete-orphan",
    )

class RipsUsuarios(Base):
    __table__ :str = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    rips_id: Mapped[int] = mapped_column(ForeignKey("rips.id"))
    tipo_documento_identificacion: Mapped[str] = mapped_column(String(2), comment="Nombre del usuario")
    num_documento_identificacion: Mapped[str] = mapped_column(String(12), comment="Numero de documento del usuario")
    tipo_usuario: Mapped[str] = mapped_column(String(2), comment="Tipo de usuario")
    fecha_nacimiento: Mapped[DateTime] = mapped_column(DateTime(),comment="Fecha Nacimiento del usuario")
    cod_sexo: Mapped[str] = mapped_column(String(1), comment="Sexo del usuario")
    cod_pais_residencia: Mapped[str] = mapped_column(String(3), comment="Codigo pais de origen del usuario")
    cod_pais_origen: Mapped[str] = mapped_column(String(3), comment="Codigo pais de origen del usuario")
    cod_municipio_residencia: Mapped[str] = mapped_column(String(5), comment="Codigo muncipio de residencia del usuario")
    cod_zona_territorial_residencia: Mapped[str] = mapped_column(String(2), comment="Codigo zona territorial de residencia del usuario")
    incapacidad: Mapped[str] = mapped_column(String(2), comment="Incapcacidad del usuario")
    registroSIRAS: Mapped[str] = mapped_column(String(20), comment="Registro SIRAS del usuario")
    consecutivo: Mapped[int] = mapped_column(Integer, comment="Consecutivo del usuario")


    rips :Mapped[list["Rips"]] = relationship("rips",back_populates="usuarios")

class RipsServicios(Base):
    __table__:str = "servicios"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    rips_id: Mapped[int] = mapped_column(ForeignKey("rips.id"))
    usuario: Mapped["RipsUsuarios"] = relationship()
