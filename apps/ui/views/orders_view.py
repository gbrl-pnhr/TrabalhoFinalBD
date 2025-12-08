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

        tab_list, tab_create = st.tabs(["Pedidos Ativos", "Nova Pedido"])

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
        dish_key = f"add_dish_sel_{order_id}"
        qty_key = f"add_qty_{order_id}"
        dish_id = st.session_state.get(dish_key)
        qty = st.session_state.get(qty_key)
        if not dish_id:
            st.toast("⚠️ Selecione um prato.")
            return
        if self.vm.add_item_to_order(order_id, dish_id, qty):
            st.toast(f"✅ Item adicionado ao pedido #{order_id}")
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
            st.info(
                "Nenhum pedido aberto encontrado. Adicione uma nova mesa para começar."
            )
            return
        df_orders = pd.DataFrame([o.model_dump() for o in orders])
        cols = ["id", "nome_cliente", "numero_mesa", "valor_total", "status"]
        display_cols = [c for c in cols if c in df_orders.columns]
        st.dataframe(
            df_orders[display_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "valor_total": st.column_config.NumberColumn(format="$%.2f"),
                "id": st.column_config.NumberColumn("Order Nº", format="%d"),
                "nome_cliente": "Cliente",
                "numero_mesa": "Mesa",
            },
        )
        st.markdown("---")
        st.subheader("Gerenciar Pedidos")
        for order in orders:
            self._render_order_card_fragment(order.id)

    @st.fragment
    def _render_order_card_fragment(self, order_id: int):
        """
        Renders a single order card.
        Crucial Update: Fetches fresh data inside the fragment to ensure
        UI consistency after add/remove operations.
        """
        order = self.vm.get_order_by_id(order_id)
        if not order or str(order.status).lower() in ["aberto", "fechado", "cancelado"]:
            return
        t_label = getattr(order, "numero_mesa", getattr(order, "id_mesa", "?"))
        c_label = getattr(order, "nome_cliente", "Desconhecido")
        w_label = getattr(order, "nome_garcom", "Desconhecido")
        label = f"📋 Pedido #{order.id} | Mesa {t_label} | {c_label}"
        with st.expander(label, expanded=False):
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.caption("Cliente")
                st.write(f"**{c_label}**")
            with col_info2:
                st.caption("Garçom Responsável")
                st.write(f"**{w_label}**")
            st.divider()
            self._render_order_items_table(order)
            st.markdown(f"**Total: R$ {order.valor_total:,.2f}**")
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
        Render items using simple table.
        """
        if not order.itens:
            st.info("Nenhum item pedido ainda.")
            return

        items_data = [
            {
                "Prato": i.nome_prato,
                "Qtd": i.quantidade,
                "Preço Un.": f"R$ {i.preco_unitario:.2f}",
                "Subtotal": f"R$ {(i.preco_unitario * i.quantidade):.2f}",
                "Obs": i.observacoes or "-",
            }
            for i in order.itens
        ]
        st.table(items_data)

    def _render_add_item_form(self, order_id: int):
        dish_options = self.vm.get_dish_options()

        c1, c2 = st.columns([3, 1])
        with c1:
            st.selectbox(
                "Escolher Prato",
                options=dish_options.keys(),
                format_func=lambda x: dish_options.get(x, "Desconhecido"),
                key=f"add_dish_sel_{order_id}",
                label_visibility="collapsed",
                placeholder="Selecione um prato...",
            )
        with c2:
            st.number_input(
                "Qtd",
                min_value=1,
                step=1,
                value=1,
                key=f"add_qty_{order_id}",
                label_visibility="collapsed",
            )

        st.button(
            "➕ Adicionar",
            key=f"btn_add_{order_id}",
            on_click=self._handle_add_item,
            args=(order_id,),
            use_container_width=True,
        )

    def _render_remove_item_form(self, order):
        if not order.itens:
            st.info("Nenhum item para remover.")
            return

        items_map = {
            item.id: f"{item.nome_prato} (x{item.quantidade})" for item in order.itens
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
                use_container_width=True,
            )

    def _render_create_order_tab(self):
        st.subheader("Novo Pedido")

        options = self.vm.get_new_order_options()
        if self.vm.last_error:
            st.error(self.vm.last_error)

        with st.form("new_order_form"):
            st.write("Adicione informações para adicionar um novo pedido:")
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
                        "Escolher Mesa",
                        options=[],
                        disabled=True,
                        key="new_order_table",
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
                "Criar Pedido",
                width="stretch",
                on_click=self._handle_create_order,
                disabled=not options.tables
            )