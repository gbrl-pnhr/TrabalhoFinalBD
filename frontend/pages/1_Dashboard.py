import streamlit as st
import pandas as pd
from frontend.services.analytics import AnalyticsService

st.set_page_config(
    page_title="Dashboard - Restaurant Manager", page_icon="📈", layout="wide"
)


def load_dashboard_data():
    """Fetch all necessary data from the API."""
    with st.spinner("Loading analytics..."):
        revenue_data = AnalyticsService.get_revenue_stats()
        dishes_data = AnalyticsService.get_popular_dishes()
        staff_data = AnalyticsService.get_waiter_performance()
    return revenue_data, dishes_data, staff_data


st.title("📈 Operational Dashboard")
st.markdown("Overview of restaurant performance, sales, and staff efficiency.")

try:
    revenue, dishes, staff = load_dashboard_data()
except Exception:
    st.error(
        "Could not connect to the Backend API. Please ensure the server is running."
    )
    st.stop()

if not revenue and not dishes and not staff:
    st.warning("No data available yet. Start taking orders to see analytics here!")
    st.stop()

total_revenue_30d = sum([item["total_revenue"] for item in revenue]) if revenue else 0.0
top_dish_name = dishes[0]["dish_name"] if dishes else "N/A"
active_waiters = len(staff) if staff else 0

col1, col2, col3 = st.columns(3)
col1.metric("Revenue (Last 30 Days)", f"${total_revenue_30d:,.2f}")
col2.metric("Top Selling Dish", top_dish_name)
col3.metric("Active Waiters", active_waiters)

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Daily Revenue Trend")
    if revenue:
        df_rev = pd.DataFrame(revenue)
        st.line_chart(df_rev, x="date", y="total_revenue", color="#2ECC71")
    else:
        st.info("No revenue data available.")

with c2:
    st.subheader("Top Popular Dishes")
    if dishes:
        df_dishes = pd.DataFrame(dishes)
        st.bar_chart(df_dishes, x="dish_name", y="quantity_sold", color="#3498DB")
    else:
        st.info("No dish data available.")

st.divider()

st.subheader("Waiter Performance")
if staff:
    df_staff = pd.DataFrame(staff)
    df_staff = df_staff[["waiter_name", "orders_handled", "total_sales"]]
    df_staff.columns = ["Name", "Orders Handled", "Total Sales Generated"]

    st.dataframe(
        df_staff,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total Sales Generated": st.column_config.NumberColumn(format="$%.2f")
        },
    )
else:
    st.info("No staff performance data available.")