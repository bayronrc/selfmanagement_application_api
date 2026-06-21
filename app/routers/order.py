from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import  get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.schemas.order import BatchCreate, OrderOut
from app.services.order_service import OrderService



router = APIRouter(prefix="/orders",tags=["orders"])


def get_order_service(db: AsyncSession = Depends(get_db))->OrderService:
    repository = OrderRepository(db)
    return OrderService(repository)

@router.post("/upload-batches")
async def upload_batch(
    payload: BatchCreate,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(get_current_user),
):
    return await service.upload_batch(payload, user.id)
