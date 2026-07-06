from datetime import  datetime
import string
from typing import List, Optional

from click.core import batch
from pydantic import BaseModel, ConfigDict, Field, field_validator


from datetime import  datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from sqlalchemy import orm


class OrderBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    fecha: Optional[datetime] = Field(None, alias="Fecha")
    id_profesional: Optional[str] = Field(None, alias="IDProfesional")
    profesional: Optional[str] = Field(None, alias="Profesional")
    no_orden: Optional[str] = Field(None, alias="NoOrden")
    codigo: Optional[str] = Field(None, alias="Codigo")
    procedimiento: Optional[str] = Field(None, alias="Procedimiento")
    cantidad: Optional[int] = Field(None, alias="Cantidad")
    dosis: Optional[str] = Field(None, alias="Dosis")
    via: Optional[str] = Field(None, alias="Via")
    dias_tto: Optional[int] = Field(None, alias="DiasTto")

    @field_validator("fecha", mode="before")
    @classmethod
    def parse_fecha(cls, v):
        if isinstance(v, str) and v.strip():
            v_clean = v.strip()
            v_clean = v_clean.replace("a. m.", "a.m.").replace("p. m.", "p.m.")
            v_clean = v_clean.replace("a.m.", "AM").replace("p.m.", "PM")

            # Lista de formatos a intentar (en orden de prioridad)
            formatos = [
                "%d/%m/%Y %I:%M:%S %p",  # 01/06/2026 02:34:00 PM
                "%d/%m/%Y %H:%M:%S",     # 01/06/2026 14:34:00
                "%Y-%m-%d %H:%M:%S",     # 2026-06-01 14:34:00
                "%d/%m/%Y",              # 01/06/2026
                "%Y-%m-%d",              # 2026-06-01
            ]

            for formato in formatos:
                try:
                    return datetime.strptime(v_clean, formato)
                except ValueError:
                    continue

            # Si ningún formato funciona, lanzar error con información útil
            raise ValueError(f"No se pudo parsear la fecha: '{v}'. Formatos soportados: {formatos}")

        if isinstance(v, datetime):
            return v

        return None

    @field_validator("dias_tto", "cantidad", mode="before")
    @classmethod
    def parse_empty_int(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v == "":
                return None
        return v

class OrderBatchCreate(BaseModel):
    filename: str
    rows : List[OrderBase]

class UploadBatchResponse(BaseModel):
    file_name : str
    total_orders: int
    batch_id : int

class OrderPaginationResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    data: List[OrderBase]
    model_config = ConfigDict(from_attributes=True)
