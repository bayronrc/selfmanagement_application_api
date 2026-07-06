import math

from fastapi import HTTPException, status
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderBatchCreate, OrderPaginationResponse, UploadBatchResponse


class OrderService:
    def __init__(self,order_repository:OrderRepository) -> None:
        self.repository = order_repository

    async def upload_batch(self, payload: OrderBatchCreate, user_id: int):
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
        await self.repository.create_orders(batch.id, rows)
        await self.repository.commit()
        return UploadBatchResponse(
            total_orders=len(rows),
            batch_id=batch.id,
            file_name=payload.filename
        )

    async def get_orders(self, user_id: int, page: int = 1 , limit: int =10, search : str| None = None):
        result = await self.repository.get_orders(user_id, page, limit, search)

        total = result["total"]
        orders = result["orders"]

        total_pages = math.ceil(total/limit) if total >0 else 0
        return OrderPaginationResponse(
            total=total,
            page=page,
            limit=limit,
            pages=total_pages,
            data=orders
        )
