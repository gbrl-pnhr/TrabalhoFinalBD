import logging
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.logging_config import setup_logging
from backend.core.database import create_pool
from backend.modules.menu.router import router as menu_router
from backend.modules.customers.router import router as customer_router
from backend.modules.tables.router import router as table_router

setup_logging()
logger = logging.getLogger("api.main")

class StateFastAPI(FastAPI):
    state: dict[str, Any]

@asynccontextmanager
async def lifespan(application: StateFastAPI):
    """
    Handles startup and shutdown events.
    The 'app' argument is injected by FastAPI and is crucial for state management.
    """
    logger.info("Application starting up...")
    application.state.pool = create_pool()
    yield
    logger.info("Application shutting down...")
    if hasattr(application.state, "pool"):
        application.state.pool.close()
        logger.info("Database connection pool closed.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu_router, prefix=settings.API_V1_STR)
app.include_router(customer_router, prefix=settings.API_V1_STR)
app.include_router(table_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "app": settings.PROJECT_NAME}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)