import streamlit as st
import plotly.express as px
from apps.ui.viewmodels.dashboard import DashboardViewModel


class DashboardView:
    """
    Handles the UI Rendering for the Dashboard Page.
    Fully translated to PT-BR and adapted for Backend PT keys.
    """

    def __init__(self, view_model: DashboardViewModel):
        self.vm = view_model

    def render(self):
        st.title("📊 Painel Geral")

        with st.spinner("Carregando dados..."):
            self.vm.load_data()

        if self.vm.has_error:
            st.error(f"⚠️ Alerta de Sistema: {self.vm.error_message}")
            if st.button("🔄 Tentar Novamente"):
                st.rerun()
            return

        self._render_kpis()
        st.divider()
        self._render_charts_row()
        st.divider()
        self._render_staff_section()
        if st.button("🔄 Recarregar Dados"):
            st.cache_data.clear()
            st.rerun()

    def _render_kpis(self):
        kpi = self.vm.get_kpi_metrics()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="Receita Total (30 Dias)",
                value=f"R${kpi.total_revenue:,.2f}",
                delta=f"R${kpi.avg_daily_revenue:,.2f} (Média Diária)",
            )
        with c2:
            st.metric(
                label="Status do Sistema",
                value="Online" if kpi.is_online else "Offline",
                delta="Conectado" if kpi.is_online else "Erro",
                delta_color="normal" if kpi.is_online else "inverse",
            )
        with c3:
            st.metric(label="Pontos de Dados", value=kpi.data_points)

    def _render_charts_row(self):
        col_rev, col_dish = st.columns([2, 1])

        with col_rev:
            self._render_revenue_chart()

        with col_dish:
            self._render_popular_dishes_chart()

    def _render_revenue_chart(self):
        st.subheader("Gráfico de Receita")
        df_rev = self.vm.get_revenue_dataframe()
        if df_rev.empty:
            st.info("Sem dados de receita disponíveis.")
            return
        fig = px.line(
            df_rev,
            x="data",
            y="receita_total",
            markers=True,
            labels={"receita_total": "Receita (R$)", "data": "Data"},
            height=350,
        )
        fig.update_xaxes(
            dtick=24 * 60 * 60 * 1000,
            tickformat="%d\n%b",
            ticklabelmode="period"
        )
        st.plotly_chart(fig)

    def _render_popular_dishes_chart(self):
        st.subheader("🍔 Pratos Mais Vendidos")
        df_dish = self.vm.get_popular_dishes_dataframe()
        if df_dish.empty:
            st.info("Sem dados de vendas.")
            return
        fig = px.bar(
            df_dish,
            x="quantidade_vendida",
            y="nome_prato",
            orientation="h",
            color="quantidade_vendida",
            color_continuous_scale="Viridis",
            labels={"quantidade_vendida": "Qtd. Vendida", "nome_prato": "Prato"},
            height=350,
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="content")

    def _render_staff_section(self):
        st.subheader("Desempenho da Equipe")
        df_staff = self.vm.get_staff_dataframe()
        if df_staff.empty:
            st.info("Nenhum registro de funcionário encontrado.")
            return
        st.dataframe(
            df_staff,
            width="stretch",
            hide_index=True,
            column_config={
                "nome_garcom": "Nome do Garçom",
                "pedidos_atentidos": "Pedidos Atendidos",
                "vendas_totais": st.column_config.NumberColumn(
                    "Vendas Totais", format="R$ %.2f"
                ),
            },
        )