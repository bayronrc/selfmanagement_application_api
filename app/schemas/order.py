from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class OrderRow(BaseModel):
    fecha: Optional[date] = Field(None, alias="Fecha")
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
            v_clean = v.replace("a. m.", "AM").replace("p. m.", "PM").replace("a.m.", "AM").replace("p.m.", "PM")
            try:
                return datetime.strptime(v_clean, "%d/%m/%Y %I:%M:%S %p").date()
            except ValueError:
                try:
                    return datetime.strptime(v_clean, "%d/%m/%Y").date()
                except ValueError:
                    return datetime.strptime(v_clean, "%Y-%m-%d").date()
        return None # Si viene vacío, devolvemos None

    # 💡 NUEVO VALIDADOR: Limpia enteros que puedan venir como strings vacíos ""
    @field_validator("dias_tto", "cantidad", mode="before")
    @classmethod
    def parse_empty_int(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v == "":
                return None # O retorna 0 si en tu DB la columna no acepta nulos
        return v

    class Config:
        populate_by_name = True


class BatchCreate(BaseModel):
    filename: str
    rows: List[OrderRow]

    class Config:
        populate_by_name = True

class OrderOut(OrderRow):
    id: int
    batch_id: int
    status: str
    error_message: Optional[str] = None
    model_config = {"from_attributes":True}
