import streamlit as st
import pandas as pd
from apps.api.modules import OrderResponse
from apps.ui.viewmodels.orders import OrdersViewModel


class OrdersView:
    """
    Handles the UI Rendering for the Orders Page.
    Uses '@st.fragment' for granular re-rendering of order cards.
    """

    def __init__(self, view_model: OrdersViewModel):
        self.vm = view_model
        if "flash_msg" not in st.session_state:
            st.session_state["flash_msg"] = None

    def render(self):
        st.title("📝 Gestor de Pedidos")

        self._handle_flash_messages()

        self.vm.load_active_orders()
        if self.vm.last_error:
            st.error(f"Erro carregando pedidos: {self.vm.last_error}")

        tab_list, tab_create = st.tabs(["Pedidos Ativos", "Nova Mesa Sendo Utilizada"])

        with tab_list:
            self._render_active_orders_tab()

        with tab_create:
            self._render_create_order_tab()

    def _handle_flash_messages(self):
        """Displays notifications stored in session_state and clears them."""
        msg = st.session_state.get("flash_msg")
        if msg:
            type_ = msg.get("type")
            text = msg.get("text")
            if type_ == "success":
                st.toast(f"✅ {text}")
            elif type_ == "error":
                st.error(f"❌ {text}")
            st.session_state["flash_msg"] = None

    def _handle_create_order(self):
        try:
            c_id = st.session_state.get("new_order_customer")
            w_id = st.session_state.get("new_order_waiter")
            t_id = st.session_state.get("new_order_table")
            count = st.session_state.get("new_order_count", 2)

            if not c_id or not w_id or not t_id:
                st.session_state["flash_msg"] = {
                    "type": "error",
                    "text": "Todos os campos são obrigatórios.",
                }
                return

            if self.vm.create_order(c_id, t_id, w_id, count):
                st.session_state["flash_msg"] = {
                    "type": "success",
                    "text": "Mesa adicionada com sucesso!",
                }
            else:
                st.session_state["flash_msg"] = {
                    "type": "error",
                    "text": self.vm.last_error,
                }
        except Exception as e:
            st.session_state["flash_msg"] = {"type": "error", "text": str(e)}

    def _handle_add_item(self, order_id: int):
        dish_key = f"add_dish_id_{order_id}"
        qty_key = f"add_qty_{order_id}"

        dish_id = st.session_state.get(dish_key)
        qty = st.session_state.get(qty_key)

        if self.vm.add_item_to_order(order_id, dish_id, qty):
            st.toast(f"✅ Item adicionado ao pedido #{order_id}")
            # Rerun to refresh the list with the new item
            st.rerun()
        else:
            st.toast(f"❌ {self.vm.last_error}")

    def _handle_remove_item(self, order_id: int):
        sel_key = f"rem_item_sel_{order_id}"
        item_id = st.session_state.get(sel_key)

        if not item_id:
            st.toast("⚠️ Nenhum item selecionado.")
            return

        if self.vm.remove_item_from_order(order_id, item_id):
            st.toast("✅ Item removido.")
            # Rerun to refresh the list (remove the item from view)
            st.rerun()
        else:
            st.toast(f"❌ {self.vm.last_error}")

    def _handle_close_order(self, order_id: int):
        if self.vm.close_order(order_id):
            st.session_state["flash_msg"] = {
                "type": "success",
                "text": f"Pedido #{order_id} concluído e pago.",
            }
            st.rerun()
        else:
            st.toast(f"❌ {self.vm.last_error}")

    def _render_active_orders_tab(self):
        orders = self.vm.active_orders
        if not orders:
            st.info("Nenhum pedido aberto encontrado. Adicione uma nova mesa para começar.")
            return

        df_orders = pd.DataFrame([o.model_dump() for o in orders])
        cols = ["id", "customer_name", "table_number", "total_value", "status"]
        display_cols = [c for c in cols if c in df_orders.columns]

        st.dataframe(
            df_orders[display_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "total_value": st.column_config.NumberColumn(format="$%.2f"),
                "id": st.column_config.NumberColumn("Order #", format="%d"),
            },
        )

        st.markdown("---")
        st.subheader("Gerenciar Pedidos")

        for order in orders:
            self._render_order_card_fragment(order)

    @st.fragment
    def _render_order_card_fragment(self, order: OrderResponse):
        """
        Renders a single order card.
        Decorated with @st.fragment to enable granular re-rendering.
        Crucial Optimization: Accepts the full 'order' object to avoid N+1 API calls.
        """
        if not order or str(order.status).lower() in ["closed", "paid", "completed"]:
            return
        t_label = getattr(order, "table_number", getattr(order, "table_id", "?"))
        label = f"📋 Pedido #{order.id} | Mesa {t_label} | R${order.total_value:,.2f}"
        with st.expander(label, expanded=False):
            self._render_order_items_table(order)
            st.divider()

            tab_add, tab_rem, tab_pay = st.tabs(
                ["Adicionar Item", "Remover Item", "Pagar e Fechar"]
            )

            with tab_add:
                self._render_add_item_form(order.id)

            with tab_rem:
                self._render_remove_item_form(order)

            with tab_pay:
                st.caption("Rever o total e prosseguir ao pagamento.")
                st.button(
                    "💰 Pagar e Fechar Pedido",
                    key=f"btn_close_{order.id}",
                    type="primary",
                    on_click=self._handle_close_order,
                    args=(order.id,),
                )

    def _render_order_items_table(self, order):
        """
        Optimized rendering using native Python dictionaries and st.table.
        Avoids Pandas overhead for small data fragments.
        """
        if not order.items:
            st.info("Nenhum item pedido ainda.")
            return
        items_data = [
            {
                "Preço": i.dish_name,
                "Quantidade": i.quantity,
                "Preço": f"${i.unit_price:.2f}",
                "Subtotal": f"${(i.unit_price * i.quantity):.2f}",
            }
            for i in order.items
        ]
        st.table(items_data)

    def _render_add_item_form(self, order_id: int):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.number_input(
                "ID do Prato", min_value=1, step=1, key=f"add_dish_id_{order_id}"
            )
        with c2:
            st.number_input(
                "Quantidade", min_value=1, step=1, value=1, key=f"add_qty_{order_id}"
            )
        with c3:
            st.write("")
            st.button(
                "Adicionar",
                key=f"btn_add_{order_id}",
                on_click=self._handle_add_item,
                args=(order_id,),
            )

    def _render_remove_item_form(self, order):
        if not order.items:
            st.info("Nenhum item para remover.")
            return

        items_map = {
            item.id: f"{item.dish_name} (x{item.quantity})" for item in order.items
        }

        c1, c2 = st.columns([3, 1])
        with c1:
            st.selectbox(
                "Selecionar Item",
                options=items_map.keys(),
                format_func=lambda x: items_map[x],
                key=f"rem_item_sel_{order.id}",
                label_visibility="collapsed",
            )
        with c2:
            st.button(
                "🗑️ Remover",
                key=f"btn_del_{order.id}",
                on_click=self._handle_remove_item,
                args=(order.id,),
            )

    def _render_create_order_tab(self):
        st.subheader("Nova Mesa Sendo Utilizada")

        options = self.vm.get_new_order_options()
        if self.vm.last_error:
            st.error(self.vm.last_error)

        with st.form("new_order_form"):
            st.write("Adicione informações para adicionar uma nova mesa:")
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(
                    "Cliente",
                    options=options.customers.keys(),
                    format_func=lambda x: options.customers.get(x, "Unknown"),
                    key="new_order_customer",
                )
                st.selectbox(
                    "Atribuir Garçom",
                    options=options.waiters.keys(),
                    format_func=lambda x: options.waiters.get(x, "Unknown"),
                    key="new_order_waiter",
                )

            with c2:
                if not options.tables:
                    st.warning("Nenhuma mesa disponível.")
                    st.selectbox(
                        "Escolher Mesa", options=[], disabled=True, key="new_order_table"
                    )
                else:
                    st.selectbox(
                        "Escolher Mesa",
                        options=options.tables.keys(),
                        format_func=lambda x: options.tables.get(x, "Unknown"),
                        key="new_order_table",
                    )

                st.number_input(
                    "Número de Pessoas",
                    min_value=1,
                    step=1,
                    value=2,
                    key="new_order_count",
                )

            st.markdown("---")
            st.form_submit_button(
                "Adicionar Mesa",
                width="stretch",
                on_click=self._handle_create_order,
                disabled=not options.tables
            )
