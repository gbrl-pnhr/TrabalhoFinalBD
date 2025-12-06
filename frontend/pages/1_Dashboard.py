import streamlit as st
from services.analytics import AnalyticsService
from components.dashboard_ui import (
    render_kpi_metrics,
    render_revenue_chart,
    render_popular_dishes_chart,
    render_staff_table,
)

# Page Config
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")


def load_data():
    """
    Aggregates data fetching.
    In a real scenario, this might use st.cache_data for performance.
    """
    with st.spinner("Fetching latest analytics..."):
        # We fetch all necessary data here
        # Failure in one shouldn't crash the others ideally,
        # but for simplicity we fetch sequentially.
        revenue = AnalyticsService.get_revenue_stats()
        dishes = AnalyticsService.get_popular_dishes()
        staff = AnalyticsService.get_staff_performance()

        # Simulate a slight delay for UX (remove in production)
        # time.sleep(0.5)

        return revenue, dishes, staff


def main():
    st.title("📊 Manager Dashboard")
    st.markdown("Real-time overview of restaurant performance.")

    # 1. Load Data
    revenue_data, dish_data, staff_data = load_data()

    # 2. Render Top KPIs
    render_kpi_metrics(revenue_data)

    st.divider()

    # 3. Render Charts Layout
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Revenue Chart
        render_revenue_chart(revenue_data)

    with col_right:
        # Top Dishes
        render_popular_dishes_chart(dish_data)

    st.divider()

    # 4. Render Staff Table
    render_staff_table(staff_data)

    # Refresh Button
    if st.button("Refresh Data"):
        st.rerun()

if __name__ == "__main__":
    main()