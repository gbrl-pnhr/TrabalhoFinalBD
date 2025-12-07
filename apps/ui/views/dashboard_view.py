import streamlit as st
import plotly.express as px
from apps.ui.viewmodels.dashboard import DashboardViewModel


class DashboardView:
    """
    Handles the UI Rendering for the Dashboard Page.
    Depends on the ViewModel for data.
    """

    def __init__(self, view_model: DashboardViewModel):
        self.vm = view_model

    def render(self):
        st.title("📊 Manager Dashboard")
        with st.spinner("Crunching numbers..."):
            self.vm.load_data()
        if self.vm.has_error:
            st.error(f"⚠️ System Alert: {self.vm.error_message}")
            if st.button("🔄 Retry Connection"):
                st.rerun()
            return
        self._render_kpis()
        st.divider()
        self._render_charts_row()
        st.divider()
        self._render_staff_section()
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()

    def _render_kpis(self):
        kpi = self.vm.get_kpi_metrics()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="Total Revenue (30 Days)",
                value=f"${kpi.total_revenue:,.2f}",
                delta=f"${kpi.avg_daily_revenue:,.2f} (Avg/Day)",
            )
        with c2:
            st.metric(
                label="System Status",
                value="Online" if kpi.is_online else "Offline",
                delta="Connected" if kpi.is_online else "Error",
                delta_color="normal" if kpi.is_online else "inverse",
            )
        with c3:
            st.metric(label="Data Points Recorded", value=kpi.data_points)

    def _render_charts_row(self):
        col_rev, col_dish = st.columns([2, 1])

        with col_rev:
            st.subheader("Revenue Trend")
            df_rev = self.vm.get_revenue_dataframe()
            if df_rev.empty:
                st.info("No revenue data available.")
            else:
                fig = px.line(
                    df_rev,
                    x="date",
                    y="total_revenue",
                    markers=True,
                    labels={"total_revenue": "Revenue ($)", "date": "Date"},
                    height=350,
                )
                st.plotly_chart(fig, width='content')

        with col_dish:
            st.subheader("🍔 Popular Dishes")
            df_dish = self.vm.get_popular_dishes_dataframe()
            if df_dish.empty:
                st.info("No sales data.")
            else:
                fig = px.bar(
                    df_dish,
                    x="total_sold",
                    y="dish_name",
                    orientation="h",
                    color="total_sold",
                    color_continuous_scale="Viridis",
                    labels={"total_sold": "Sold", "dish_name": ""},
                    height=350,
                )
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, width='content')

    def _render_staff_section(self):
        st.subheader("Staff Performance")
        df_staff = self.vm.get_staff_dataframe()
        if df_staff.empty:
            st.info("No staff records found.")
        else:
            st.dataframe(
                df_staff,
                width='content',
                hide_index=True,
                column_config={
                    "waiter_id": "ID",
                    "waiter_name": "Name",
                    "orders_count": "Orders Handled",
                    "total_sales": st.column_config.NumberColumn(
                        "Total Sales", format="$%.2f"
                    ),
                },
            )