from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.order_repository import OrderRepository
from app.schemas.order import BatchCreate


class OrderService:
    def __init__(self,order_repository:OrderRepository) -> None:
        self.repository = order_repository

    async def upload_batch(self, payload: BatchCreate, user_id: int):
        if not payload.rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no tiene filas"
            )

        batch = await self.repository.create_batch(
            filename=payload.filename,
            uploaded_by=user_id
        )
        rows = [row.model_dump() for row in payload.rows]
        orders = await self.repository.create_orders(batch.id, rows)
        await self.repository.commit()
        return { "batch": batch, "orders": orders}
