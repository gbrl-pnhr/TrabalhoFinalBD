from typing import List, Dict, Any, Tuple
import pandas as pd


def calculate_revenue_metrics(
    revenue_data: List[Dict[str, Any]],
) -> Tuple[float, float, int]:
    """
    Calculates Total Revenue, Average Daily Revenue, and Count from raw data.

    Returns:
        Tuple[float, float, int]: (Total Revenue, Average Revenue, Data Points Count)
    """
    if not revenue_data:
        return 0.0, 0.0, 0

    df = pd.DataFrame(revenue_data)

    if "total_revenue" not in df.columns:
        return 0.0, 0.0, 0

    total = df["total_revenue"].sum()
    avg = df["total_revenue"].mean()
    count = len(df)

    return total, avg, count