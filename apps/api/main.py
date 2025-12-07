import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.config import settings
from db.connection import create_db_pool

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from apps.api.modules.menu.router import router as menu_router
from apps.api.modules.customers.router import router as customer_router
from apps.api.modules.tables.router import router as table_router
from apps.api.modules.staff.routers import router as staff_router
from apps.api.modules.orders.router import router as order_router
from apps.api.modules.reviews.router import router as review_router
from apps.api.modules.analytics.router import router as analytics_router
from packages.common.src.log_config import setup_logging

setup_logging(app_name="api", log_dir=Path("logs"))
logger = logging.getLogger("api.main")

class StateFastAPI(FastAPI):
    state: dict[str, Any]

@asynccontextmanager
async def lifespan(application: StateFastAPI):
    logger.info("Application starting up...")
    application.state.pool = await create_db_pool()
    yield
    logger.info("Application shutting down...")
    if hasattr(application.state, "pool"):
        await application.state.pool.close()
        logger.info("Database connection pool closed.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/v1/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(table_router, prefix="/api/v1")
app.include_router(staff_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(review_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)