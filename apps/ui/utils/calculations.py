from typing import List, Tuple
import pandas as pd
from apps.ui.schemas import DailyRevenue

def calculate_revenue_metrics(
    revenue_data: List[DailyRevenue],
) -> Tuple[float, float, int]:
    """
    Calculates Total Revenue, Average Daily Revenue, and Count from typed data.

    Returns:
        Tuple[float, float, int]: (Total Revenue, Average Revenue, Data Points Count)
    """
    if not revenue_data:
        return 0.0, 0.0, 0
    df = pd.DataFrame([r.model_dump() for r in revenue_data])
    if "total_revenue" not in df.columns:
        return 0.0, 0.0, 0
    total = df["total_revenue"].sum()
    avg = df["total_revenue"].mean()
    count = len(df)
    return total, avg, count