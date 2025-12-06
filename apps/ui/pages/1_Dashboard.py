import streamlit as st
from apps.ui.services.analytics import AnalyticsService
from apps.ui.utils.calculations import calculate_revenue_metrics
from apps.ui.utils.exceptions import APIConnectionError
from apps.ui.components.dashboard_ui import (
    render_kpi_metrics,
    render_revenue_chart,
    render_popular_dishes_chart,
    render_staff_table,
)


@st.cache_data(ttl=60, show_spinner="Fetching latest analytics...")
def load_dashboard_data():
    analytics_service = AnalyticsService()
    try:
        revenue = analytics_service.get_revenue_stats()
        dishes = analytics_service.get_popular_dishes()
        staff = analytics_service.get_staff_performance()
        return revenue, dishes, staff
    except APIConnectionError:
        return None, None, None
    except Exception as e:
        return "error", str(e), None

def main():
    st.title("📊 Manager Dashboard")
    revenue_data, dish_data, staff_data = load_dashboard_data()
    if revenue_data is None:
        st.error("⚠️ Backend is offline. Please check your connection.")
        if st.button("Retry Connection"):
            st.cache_data.clear()
            st.rerun()
        return
    elif revenue_data == "error":
        st.error(f"⚠️ Error loading data: {dish_data}")
        return
    total_rev, avg_rev, count = calculate_revenue_metrics(revenue_data)
    render_kpi_metrics(total_rev, avg_rev, count)
    st.divider()
    col_left, col_right = st.columns([2, 1])
    with col_left:
        render_revenue_chart(revenue_data)
    with col_right:
        render_popular_dishes_chart(dish_data)
    st.divider()
    render_staff_table(staff_data)
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

main()