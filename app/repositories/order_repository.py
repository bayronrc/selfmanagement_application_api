from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderBatch

class OrderRepository:
    def __init__(self,db: AsyncSession) -> None:
        self.db = db

    async def create_batch(self, filename: str, uploaded_by: int)->OrderBatch:
        batch = OrderBatch(file_name=filename, uploaded_by=uploaded_by)
        self.db.add(batch)
        await self.db.flush()
        return batch

    async def create_orders(self, batch_id:int, rows: list[dict]):
        valid_columns = {c.name for c in Order.__table__.columns}

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

    async def commit(self):
        await self.db.commit()
