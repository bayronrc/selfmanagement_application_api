from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator


class OrderRow(BaseModel):
    fecha: Optional[date] = None
    id_profesional: Optional[str] = None
    profesional: Optional[str] = None
    no_orden: Optional[str] = None
    codigo: Optional[str] = None
    procedimiento: Optional[str] = None
    cantidad: Optional[int] = None
    dosis: Optional[str] = None
    via: Optional[str] = None
    dias_tto: Optional[int] = None

    @field_validator("fecha", mode="before")
    @classmethod
    def parse_fecha(cls,v):
        if isinstance(v,str):
            from datetime import datetime
            return datetime.strptime(v,"%Y-%m-%d").date()
        return v

class BatchCreate(BaseModel):
    file_name: str
    rows: list[OrderRow]

class OrderOut(OrderRow):
    id: int
    batch_id: int
    status: str
    error_message: Optional[str] = None
    model_config = {"from_attributes":True}
