import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Dict, Any


def render_kpi_metrics(revenue_data: List[Dict[str, Any]], order_count: int = 0):
    """
    Renders the top-level KPI cards (Total Revenue, Trends).
    """
    if not revenue_data or isinstance(revenue_data, dict) and "error" in revenue_data:
        st.error("Could not load KPI data.")
        return

    df = pd.DataFrame(revenue_data)

    # Calculate totals
    total_revenue = df["total_revenue"].sum() if not df.empty else 0.0

    # Calculate simple trend (last day vs average)
    avg_revenue = df["total_revenue"].mean() if not df.empty else 0.0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Revenue (30 Days)",
            value=f"${total_revenue:,.2f}",
            delta=f"${avg_revenue:,.2f} (Avg)",
        )

    with col2:
        # Placeholder for real-time active orders if we had that endpoint handy here
        st.metric(label="Active Orders context", value="See Orders Tab")

    with col3:
        st.metric(label="Data Points", value=len(df))


def render_revenue_chart(revenue_data: List[Dict[str, Any]]):
    """
    Renders a line chart for daily revenue.
    """
    st.subheader("💰 Revenue Trend")

    if not revenue_data:
        st.info("No revenue data available.")
        return

    df = pd.DataFrame(revenue_data)

    if df.empty:
        st.warning("Empty dataset.")
        return

    # Ensure date parsing
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    fig = px.line(
        df,
        x="date",
        y="total_revenue",
        markers=True,
        title="Daily Revenue (Last 30 Days)",
        labels={"total_revenue": "Revenue ($)", "date": "Date"},
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)


def render_popular_dishes_chart(dish_data: List[Dict[str, Any]]):
    """
    Renders a horizontal bar chart for top selling items.
    """
    st.subheader("🍔 Popular Dishes")

    if not dish_data:
        st.info("No dish data available.")
        return

    df = pd.DataFrame(dish_data)
    if df.empty:
        st.warning("No sales recorded yet.")
        return

    fig = px.bar(
        df,
        x="quantity_sold",
        y="dish_name",
        orientation="h",
        title="Top 10 Dishes by Quantity Sold",
        labels={"quantity_sold": "Quantity Sold", "dish_name": "Dish"},
        color="quantity_sold",
        color_continuous_scale="Viridis",
    )
    # Invert y-axis to show top item at the top
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def render_staff_table(staff_data: List[Dict[str, Any]]):
    """
    Renders a clean table for staff performance.
    """
    st.subheader("👨‍🍳 Staff Performance")

    if not staff_data:
        st.info("No staff data available.")
        return

    df = pd.DataFrame(staff_data)
    if df.empty:
        st.warning("No staff performance records.")
        return

    # Rename columns for display
    display_df = df.rename(
        columns={
            "name": "Waiter Name",
            "orders_count": "Orders Handled",
            "total_sales": "Total Sales Generated",
        }
    )

    # Format currency
    st.dataframe(
        display_df,
        column_config={
            "Total Sales Generated": st.column_config.NumberColumn(
                "Total Sales", format="$%.2f"
            )
        },
        use_container_width=True,
        hide_index=True,
    )