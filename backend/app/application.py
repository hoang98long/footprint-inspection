"""FastAPI application composition and lifecycle."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config.settings import settings
from app.database.session import initialise_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Chỉ dùng khi khởi tạo môi trường phát triển có PostgreSQL sẵn sàng.
    # Production phải áp dụng migration Alembic trước khi chạy service.
    if settings.auto_create_schema:
        initialise_database()
    yield


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["system"])
    def load_balancer_health_check() -> dict[str, str]:
        """Endpoint không version hoá cho Docker, load balancer và monitoring."""
        return {"status": "ok", "service": "footprint-inspection-api"}

    return app
