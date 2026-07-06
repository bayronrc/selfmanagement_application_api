
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import  get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderBatchCreate, OrderPaginationResponse, UploadBatchResponse
from app.services.order_service import OrderService



router = APIRouter(prefix="/orders",tags=["orders"])


def get_order_service(db: AsyncSession = Depends(get_db))->OrderService:
    repository = OrderRepository(db)
    return OrderService(repository)

@router.post(
        "/upload-batches",
        response_model=UploadBatchResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Crear lote de ordenes",
        description="Crea un lote de ordenes"
        )
async def upload_batch(
    payload:OrderBatchCreate,
    service: OrderService = Depends(get_order_service),
    user: User = Depends(get_current_user),
):
    return await service.upload_batch(payload, user.id)

@router.get("/get-orders",
            response_model=OrderPaginationResponse,
            status_code=status.HTTP_200_OK,
            summary="Obtener Listado de Ordenes",
            description="Retorna todas las ordenes registradas en el sistema",
)
async def get_orders(
    page: int,
    limit: int,
    search: str | None = None,
    user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return await service.get_orders(user.id, page, limit, search)
