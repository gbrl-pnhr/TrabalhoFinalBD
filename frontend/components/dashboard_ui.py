import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List
from schemas import DailyRevenue, DishPopularity, WaiterPerformance


def render_kpi_metrics(total_revenue: float, avg_revenue: float, data_points: int):
    """Renders the top-level KPI cards."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Revenue (30 Days)",
            value=f"${total_revenue:,.2f}",
            delta=f"${avg_revenue:,.2f} (Avg/Day)",
        )
    with col2:
        st.metric(label="System Status", value="Online")
    with col3:
        st.metric(label="Data Points Recorded", value=data_points)


def render_revenue_chart(revenue_data: List[DailyRevenue]):
    """Renders a line chart for daily revenue."""
    st.subheader("Revenue Trend")
    if not revenue_data:
        st.info("No revenue data available.")
        return
    df = pd.DataFrame([r.model_dump() for r in revenue_data])
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    fig = px.line(
        df,
        x="date",
        y="total_revenue",
        markers=True,
        title="Daily Revenue",
        labels={"total_revenue": "Revenue ($)", "date": "Date"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_popular_dishes_chart(dish_data: List[DishPopularity]):
    st.subheader("🍔 Popular Dishes")
    if not dish_data:
        st.info("No sales data yet.")
        return
    df = pd.DataFrame([d.model_dump() for d in dish_data])
    if df.empty:
        st.warning("No sales recorded yet.")
        return
    fig = px.bar(
        df,
        x="quantity_sold",
        y="dish_name",
        orientation="h",
        title="Top Selling Items",
        color="quantity_sold",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def render_staff_table(staff_data: List[WaiterPerformance]):
    st.subheader("Staff Performance")
    if not staff_data:
        st.info("No staff records found.")
        return
    df = pd.DataFrame([s.model_dump() for s in staff_data])
    st.dataframe(df, use_container_width=True, hide_index=True)