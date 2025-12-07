import streamlit as st
import time
from apps.ui.viewmodels.kitchen import KitchenViewModel, KitchenTicket


class KitchenView:
    """
    Handles the UI Rendering for the Kitchen Display System (KDS).
    Strictly presentation logic; delegates data ops to KitchenViewModel.
    """

    def __init__(self, view_model: KitchenViewModel):
        self.vm = view_model

    def render(self):
        st.title("🍳 Sistema de Cozinha")
        top_col, _ = st.columns([6, 1])
        with top_col:
            st.caption("Feed Automático • Recarrega a cada 30s")
        content_placeholder = st.empty()
        self.vm.load_orders()
        with content_placeholder.container():
            if self.vm.last_error:
                st.error(f"🔌 Conexão Perdida: {self.vm.last_error}")
            elif not self.vm.tickets:
                self._render_empty_state()
            else:
                self._render_ticket_grid()
        st.markdown("---")
        c1, c2 = st.columns([6, 1])
        with c1:
            if self.vm.last_updated:
                st.caption(f"Última atualização: {self.vm.last_updated}")
        with c2:
            if st.button("🔄 Recarregar"):
                st.rerun()

    def _render_empty_state(self):
        st.success("✅ Todos os pedidos entregues! A cozinha está calma.")

    def _render_ticket_grid(self):
        COLUMNS_PER_ROW = 3
        tickets = self.vm.tickets

        for i in range(0, len(tickets), COLUMNS_PER_ROW):
            row_tickets = tickets[i : i + COLUMNS_PER_ROW]
            cols = st.columns(COLUMNS_PER_ROW)

            for col, ticket in zip(cols, row_tickets):
                with col:
                    self._render_ticket(ticket)

    def _render_ticket(self, ticket: KitchenTicket):
        """
        Renders a single ticket card.
        Moved here from components/cards.py for better cohesion.
        """

        with st.container(border=True):
            # Header
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"### 🍽️ Mesa {ticket.table_label}")
                st.caption(f"#{ticket.order_id} • {ticket.waiter_label}")
            with c2:
                st.markdown(f"**{ticket.time_elapsed_label}**")
                if ticket.is_alert:
                    st.markdown("🔥 **ATRASADO**")
                else:
                    st.markdown("🔴 PREPARANDO")

            st.divider()

            # Body
            if not ticket.items:
                st.warning("Pedido Vazio")
            else:
                for item in ticket.items:
                    st.markdown(f"#### **{item.quantity}x** {item.dish_name}")
                    if item.notes:
                        st.caption(f"📝 {item.notes}")