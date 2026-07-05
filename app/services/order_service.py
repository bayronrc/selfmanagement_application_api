from fastapi import HTTPException, status
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
        return { "batch": batch ,"orders": orders}

    async def get_orders(self, user_id: int, page: int , limit: int):
        result = await self.repository.get_orders(user_id, page, limit)

        total = result["total"]
        orders = result["orders"]

        total_pages = (total + limit - 1 )
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": total_pages,
            "data": orders
        }
