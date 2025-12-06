import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from apps.api.core.database import get_db_connection
from apps.api.modules.analytics.models import (
    DailyRevenue,
    DishPopularity,
    WaiterPerformance,
)
from apps.api.modules.analytics.repository import AnalyticsRepository

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)


def get_repository(conn=Depends(get_db_connection)):
    """Dependency injection for AnalyticsRepository."""
    return AnalyticsRepository(conn)


@router.get("/revenue", response_model=List[DailyRevenue])
def get_revenue_stats(repo: AnalyticsRepository = Depends(get_repository)):
    """
    Get daily revenue statistics for the last 30 days.
    """
    try:
        return repo.get_daily_revenue()
    except Exception as e:
        logger.error(f"Error fetching revenue stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/popular-dishes", response_model=List[DishPopularity])
def get_popular_dishes(repo: AnalyticsRepository = Depends(get_repository)):
    """
    Get top 10 most popular dishes based on quantity sold.
    """
    try:
        return repo.get_top_dishes()
    except Exception as e:
        logger.error(f"Error fetching popular dishes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get("/staff-performance", response_model=List[WaiterPerformance])
def get_staff_stats(repo: AnalyticsRepository = Depends(get_repository)):
    """
    Get performance statistics (orders handled, total sales) for waiters.
    """
    try:
        return repo.get_waiter_performance()
    except Exception as e:
        logger.error(f"Error fetching staff stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )