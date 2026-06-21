from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.routers.order import router as order_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Autogestion de Ordenes y Citas API",
    docs_url="/",

    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     print(exc.errors())
#     print(request)
#     return JSONResponse(status_code=422,content={"detail":exc.errors()})
app.include_router(order_router)
