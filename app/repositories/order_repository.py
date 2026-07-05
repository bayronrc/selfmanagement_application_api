from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderBatch

class OrderRepository:
    def __init__(self,db: AsyncSession) -> None:
        self.db = db
        self.model = Order
        self.order_batch_model = OrderBatch

    async def create_batch(self, filename: str, uploaded_by: int)->OrderBatch:
        batch = OrderBatch(file_name=filename, uploaded_by=uploaded_by)
        self.db.add(batch)
        await self.db.flush()
        return batch

    async def create_orders(self, batch_id:int, rows: list[dict]):
        valid_columns = {c.name for c in self.order_batch_model.__table__.columns}

        orders = []
        for row in rows:
            filtered_row = {k: v for k, v in row.items() if k in valid_columns}

            if filtered_row.get("fecha")is not None:
                order_instance = Order(
                    batch_id=batch_id,
                    **filtered_row
                )
                orders.append(order_instance)

        self.db.add_all(orders)
        await self.db.flush()
        return orders

    async def get_orders(self, user_id : int, page: int, limit: int):
        offset = (page - 1 ) * limit
        count_query = (
            select(func.count(1))
            .select_from(self.model)
            .join(self.order_batch_model, self.model.batch_id == self.order_batch_model.id)
            .where(self.order_batch_model.uploaded_by == user_id)
        )

        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        data_query = (
            select(self.model)
            .join(self.order_batch_model, self.model.batch_id == self.order_batch_model.id)
            .where(self.order_batch_model.uploaded_by ==user_id)
            .order_by(self.model.id.desc())
            .limit(limit)
            .offset(offset)
        )

        data_result = await self.db.execute(data_query)
        orders = data_result.scalars().all()

        return { "total": total , "orders": orders}


    async def commit(self):
        await self.db.commit()
