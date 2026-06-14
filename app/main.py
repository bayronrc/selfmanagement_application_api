from fastapi import FastAPI
from app.core.config import settings
from app.routers.order import router as order_router

app = FastAPI()

app.include_router(order_router)
