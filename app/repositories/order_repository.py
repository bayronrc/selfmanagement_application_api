from sqlalchemy.orm import Session

from app.models.order import Order, OrderBatch

class OrderRepository:
    def __init__(self,db: Session) -> None:
        self.db = db

    def create_batch(self, filename: str, uploaded_by: int)->OrderBatch:
        batch = OrderBatch(filename=filename, uploaded_by=uploaded_by)
        self.db.add(batch)
        self.db.flush()
        return batch

    def create_orders(self, batch_id:int, rows: list[dict]):
        orders = [Order(batch_id=batch_id,**row) for row in rows]
        self.db.add_all(orders)
        return orders
