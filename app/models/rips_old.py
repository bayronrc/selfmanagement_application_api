
from enum import Enum as PyEnum
from typing import Optional
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RipsOldStatus(str, PyEnum):
    REVISADO = "revisado"
    PENDIENTE = "pendiente"
    AUDITADO = "auditado"


class RipsOld(Base):
    __tablename__ = "rips_old"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uploaded_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[Optional[RipsOldStatus]] = mapped_column(Enum(RipsOldStatus, name="rips_status"),
                                                  default=RipsOldStatus.PENDIENTE, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Rips(Base):
    __tablename__: str = "rips"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    num_documento_id_obligatorio: Mapped[str] = mapped_column(String(12),comment="Numero NIT con el cual se indetifique el facturador electronico")
    num_factura: Mapped[str] = mapped_column(String(20), comment="Numero de factura")
    tipo_nota: Mapped[Optional[str]] = mapped_column(String(2), nullable=True, comment="tipo nota")
    num_nota: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="numero de nota")
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuarios: Mapped[list["RipsUsuarios"]] = relationship(
        back_populates="rips",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class RipsUsuarios(Base):
    __tablename__: str = "rips_usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rips_id: Mapped[int] = mapped_column(ForeignKey("rips.id"))
    tipo_documento_identificacion: Mapped[str] = mapped_column(String(2), comment="Nombre del usuario")
    num_documento_identificacion: Mapped[str] = mapped_column(String(12), comment="Numero de documento del usuario")
    tipo_usuario: Mapped[str] = mapped_column(String(2), comment="Tipo de usuario")
    fecha_nacimiento: Mapped[DateTime] = mapped_column(DateTime(timezone=True), comment="Fecha Nacimiento del usuario")
    cod_sexo: Mapped[str] = mapped_column(String(1), comment="Sexo del usuario")
    cod_pais_residencia: Mapped[str] = mapped_column(String(3), comment="Codigo pais de origen del usuario")
    cod_pais_origen: Mapped[str] = mapped_column(String(3), comment="Codigo pais de origen del usuario")
    cod_municipio_residencia: Mapped[str] = mapped_column(String(5),
                                                          comment="Codigo muncipio de residencia del usuario")
    cod_zona_territorial_residencia: Mapped[str] = mapped_column(String(2),
                                                                 comment="Codigo zona territorial de residencia del usuario")
    incapacidad: Mapped[str] = mapped_column(String(2), comment="Incapcacidad del usuario")
    registroSIRAS: Mapped[str] = mapped_column(String(20), comment="Registro SIRAS del usuario")
    consecutivo: Mapped[int] = mapped_column(Integer, comment="Consecutivo del usuario")

    rips: Mapped[list["Rips"]] = relationship("rips", back_populates="usuarios")


class RipsServicios(Base):
    __tablename__: str = "rips_servicios"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rips_id: Mapped[int] = mapped_column(ForeignKey("rips.id"))

    rips_usuarios_id: Mapped["RipsUsuarios"] = relationship(
        back_populates="servicios",
    )

    procedimientos: Mapped[list["RipsProcedimiento"]] = relationship(
        "servicios",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    consultas : Mapped[list["RipsConsulta"]] = relationship(
        "servicios",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class RipsConsulta(Base):
    __tablename__: str = "rips_consultas"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    servicios_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rips_servicios.id", ondelete="CASCADE"), nullable=True, index=True)
    cod_prestador: Mapped[str] = mapped_column(String(12), comment="Codigo del prestador")
    fecha_inicio_atencion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), comment="Fecha de inicio de atencion")
    num_authorizacion: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Numero de autorizacion")
    cod_consulta: Mapped[str] = mapped_column(String(6), comment="Codigo de la consulta")
    modalidad_grupo_servicio_tec_sal: Mapped[str] = mapped_column(String(2), comment="Determina la forma de prestar un servicio de salud en condiciones particulares en relacion con el grupo de servicios")
    grupo_servicios: Mapped[str] = mapped_column(String(2), comment="Representa la agrupacion de servicios que se encuentran relacionados con un procedimiento de salud")

    cod_servicio: Mapped[int] = mapped_column(Integer,comment="Codigo de servicio")
    finalidad_tec_salud: Mapped[str] = mapped_column(String(2), comment="Identificador de la finalidad con la que se realiza un procedimiento")
    causa_motivo_atencion:Mapped[str] = mapped_column(String(2), comment="Identificador de la causa o motivo de atencion")

    cod_diagnostico_principal: Mapped[str] = mapped_column(String(4),comment="Codigo del diagnosttico principal (CIE-10)")
    cod_diagnostico_principal_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Codigo del diagnostico principal (CIE-11)")
    nom_cod_diagnostico_principal_cie11: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Nombre correspondiente al diagnostico principal cie11")

    cod_diagnostico_relacionado1: Mapped[Optional[str]] = mapped_column(String(4), nullable=True, comment="Codigo del diagnostico relacionado 1 (CIE-10)")
    cod_diagnostico_relacionado1_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Codigo del diagnostico relacionado 1 (CIE-11)")
    nom_cod_diagnostico_relacionado1_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Nombre correspondiente al diagnostico relacionado 1 cie11")

    cod_diagnostico_relacionado2: Mapped[Optional[str]] = mapped_column(String(4), nullable=True, comment="Codigo del diagnostico relacionado 2 (CIE-10)")
    cod_diagnostico_relacionado2_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Codigo del diagnostico relacionado 2 (CIE-11)")
    nom_cod_diagnostico_relacionado2_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Nombre correspondiente al diagnostico relacionado 2 cie11")

    cod_diagnostico_relacionado3: Mapped[Optional[str]] = mapped_column(String(4), nullable=True, comment="Codigo del diagnostico relacionado 2 (CIE-10)")
    cod_diagnostico_relacionado3_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Codigo del diagnostico relacionado 2 (CIE-11)")
    nom_cod_diagnostico_relacionado3_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Nombre correspondiente al diagnostico relacionado 2 cie11")

    tipo_diagnostico_principal: Mapped[str] = mapped_column(String(2), comment="Identificador del tipo de diagnostico principal")

    tipo_documento_identificacion: Mapped[str] = mapped_column(String(2), comment="Tipo de documento de indentificacion del profesional que ordeno o realizo el procedimiento")
    num_documenento_identificacion: Mapped[str] = mapped_column(String(20), comment="Numero de documento de indentificacion del profesional que ordeno o realizo el procedimiento")

    valor_servicio: Mapped[Integer] = mapped_column(Integer, comment="Valor del servicio")
    concepto_recaudo: Mapped[str] = mapped_column(String(2), comment="Concepto de recaudo")
    valor_pago_moderador: Mapped[Integer] = mapped_column(Integer(), comment="Valor del pago moderador")
    num_fev_pago_moderador: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Numero de FEV del pago moderador")
    codigo_vida: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Codigo de vida")
    consecutivo: Mapped[int] = mapped_column(Integer(), comment="Consecutivo del procedimiento")

    servicios : Mapped[list["RipsServicios"]] = relationship(
        back_populates="consultas",
    )




class RipsProcedimiento(Base):
    __tablename__:str = "rips_procedimientos"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    cod_prestador: Mapped[str] = mapped_column(String(12), comment="Codigo del prestador")

    servicios_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rips_servicios.id", ondelete="CASCADE"), nullable=True,index=True)
    cod_prestador: Mapped[str] = mapped_column(String(20), comment="Codigo del prestador")
    fecha_inicio_atencion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), comment="Fecha de inicio de atencion")
    id_mipres: Mapped[Optional[str]] = mapped_column(String(30),nullable=True, comment="Id mipres")
    num_autorizacion: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Numero de autorizacion")
    cod_procedimiento: Mapped[str] = mapped_column(String(10), comment="Codigo del procedimiento")
    via_ingreso_servicio_salud: Mapped[str] = mapped_column(String(2), comment="Via de ingreso del servicio de salud")
    madalidad_grupo_servicio_tec_sal: Mapped[str] = mapped_column(String(2),comment="Determina la forma de prestar un servicio de salud en codiciones particulares en relacion con el grupo de servicios")
    grupo_servicios : Mapped[str] = mapped_column(String(2), comment="Representa la agrupacion de servcios que se encuentran relacionados con un procedimiento de salud")
    cod_servicio: Mapped[int] = mapped_column(Integer, comment="Codigo de servicio")
    finalidad_tec_salud: Mapped[str] = mapped_column(String(2), comment="Identificador de la finalidad con la que se realiza un procedidmiento")

    tipo_documento_identificacion: Mapped[str] = mapped_column(String(2), comment="Tipo de documento de indentificacion del profesional que ordeno o realizo el procedimiento")
    num_documenento_identificacion: Mapped[str] = mapped_column(String(20), comment="Numero de documento de indentificacion del profesional que ordeno o realizo el procedimiento")

    cod_diagnostico_principal: Mapped[str] = mapped_column(String(10), comment="Codigo del diagnostico principal (CIE-10)")
    cod_diagnostico_principal_cie11: Mapped[Optional[str]] = mapped_column(String(255),nullable=True, comment="Codigo del diagnostico principal (CIE-11)")
    nom_cod_diganostico_principal_cie11: Mapped[Optional[str]] = mapped_column(Text,nullable=True, comment="Nombre correspondiente al diagnostico principal cie11")

    cod_diagnostico_relacionado: Mapped[Optional[str]] = mapped_column(String(4), nullable=True, comment="Codigo del diagnostico relacionado (CIE-10)")
    cod_diagnostico_relacionado_cie11: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="Codigo del diagnostico relacionado (CIE-11)")
    nom_cod_diagnostico_relacionado_cie11: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="Nombre correspondiente al diagnostico relacionado cie11")

    cod_complicacion: Mapped[Optional[str]] = mapped_column(String(4), nullable=True, comment="Codigo del diagnostico de complicacion (CIE-10)")
    cod_complicacion_cie11: Mapped[Optional[str]] = mapped_column(Text,nullable=True, comment="Codigo del diagnostico de complicacion (CIE-11)")
    nom_cod_complicacion_cie11: Mapped[Optional[str]] = mapped_column(Text,nullable=True, comment="Nombre correspondiente al diagnostico de complicacion cie11")

    vr_servicio : Mapped[Integer] = mapped_column(Integer, comment="Valor del servicio")
    concepto_recaudo: Mapped[str] = mapped_column(String(2), comment="Concepto de recaudo")
    valor_pago_moderador: Mapped[Integer] = mapped_column(Integer, comment="Valor del pago moderador")
    num_fev_pago_moderador: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, comment="Numero de FEV del pago moderador")
    codigo_vida: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="Codigo de vida")
    consecutivo: Mapped[int] = mapped_column(Integer, comment="Consecutivo del procedimiento")

    servicios: Mapped[list["RipsServicios"]] = relationship(
        back_populates="procedimientos",
    )
