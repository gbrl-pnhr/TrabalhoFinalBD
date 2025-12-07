from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from dataclasses import dataclass
from apps.ui.services.analytics import AnalyticsService
from apps.api.modules import DailyRevenue, DishPopularity, WaiterPerformance
from apps.ui.utils.exceptions import AppError


@dataclass
class KPIMetrics:
    total_revenue: float
    avg_daily_revenue: float
    data_points: int
    is_online: bool


class DashboardViewModel:
    """
    Business Logic for the Dashboard.
    Optimized with Threading for parallel data fetching.
    """

    def __init__(self, analytics_service: AnalyticsService):
        self._service = analytics_service
        self._revenue_data: List[DailyRevenue] = []
        self._popular_dishes: List[DishPopularity] = []
        self._staff_performance: List[WaiterPerformance] = []
        self._error: Optional[str] = None

    def load_data(self) -> None:
        """
        Fetches all required data from the backend IN PARALLEL.
        This significantly reduces load time by running 3 requests simultaneously.
        """
        self._error = None
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_rev = executor.submit(self._service.get_revenue_stats)
            future_dish = executor.submit(self._service.get_popular_dishes)
            future_perf = executor.submit(self._service.get_staff_performance)
            try:
                self._revenue_data = future_rev.result()
                self._popular_dishes = future_dish.result()
                self._staff_performance = future_perf.result()
            except AppError as e:
                self._error = str(e)
            except Exception as e:
                self._error = f"Unexpected error loading dashboard: {str(e)}"

    @property
    def has_error(self) -> bool:
        return self._error is not None

    @property
    def error_message(self) -> str:
        return self._error or ""

    def get_kpi_metrics(self) -> KPIMetrics:
        """Calculates top-level numbers."""
        if not self._revenue_data:
            return KPIMetrics(0.0, 0.0, 0, is_online=not self.has_error)

        total = sum(r.receita_total for r in self._revenue_data)
        count = len(self._revenue_data)
        avg = total / count if count > 0 else 0.0

        return KPIMetrics(
            total_revenue=total,
            avg_daily_revenue=avg,
            data_points=count,
            is_online=not self.has_error,
        )

    def get_revenue_dataframe(self) -> pd.DataFrame:
        """Prepares the DataFrame for the Revenue Line Chart."""
        if not self._revenue_data:
            return pd.DataFrame(columns=["date", "total_revenue"])

        df = pd.DataFrame([r.model_dump() for r in self._revenue_data])
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df

    def get_popular_dishes_dataframe(self) -> pd.DataFrame:
        """Prepares the DataFrame for the Popular Dishes Bar Chart."""
        if not self._popular_dishes:
            return pd.DataFrame(columns=["dish_name", "total_sold"])

        df = pd.DataFrame([d.model_dump() for d in self._popular_dishes])
        # Sort for better chart visualization
        return df.sort_values("total_sold", ascending=True)

    def get_staff_dataframe(self) -> pd.DataFrame:
        """Prepares the DataFrame for the Staff Table."""
        if not self._staff_performance:
            return pd.DataFrame()
        return pd.DataFrame([s.model_dump() for s in self._staff_performance])