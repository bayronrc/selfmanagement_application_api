from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.order_repository import OrderRepository
from app.schemas.order import BatchCreate
class OrderService:
    def __init__(self,db: Session) -> None:
        self.repository = OrderRepository(db)
        self.db = db

    def upload_batch(self, payload: BatchCreate, user_id: int):
        if not payload.rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no tiene filas"
            )
        no_ordenes = [r.no_orden for r in payload.rows if r.no_orden]
        if len(no_ordenes) != len(set(no_ordenes)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hay Ordenes duplicadas"
            )
        batch = self.repository.create_batch(
            filename=payload.file_name,
            uploaded_by=user_id
        )
        rows = [row.model_dump()for row in payload.rows]
        orders = self.repository.create_orders(batch.id,rows)
        self.db.commit()
        return {"batch": batch, "orders": orders}
