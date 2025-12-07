import streamlit as st
import pandas as pd
import time
from apps.ui.viewmodels.orders import OrdersViewModel


class OrdersView:
    """
    Handles the UI Rendering for the Orders Page.
    Owns all presentation logic: Cards, Forms, and Lists.
    """

    def __init__(self, view_model: OrdersViewModel):
        self.vm = view_model

    def render(self):
        st.header("📝 Order Management")

        # Initial Data Load
        self.vm.load_active_orders()

        if self.vm.last_error:
            st.error(f"Error loading orders: {self.vm.last_error}")

        tab_list, tab_create = st.tabs(["Active Orders", "Open New Table"])

        with tab_list:
            self._render_active_orders_tab()

        with tab_create:
            self._render_create_order_tab()

    def _render_active_orders_tab(self):
        orders = self.vm.active_orders
        if not orders:
            st.info("No active orders found. Open a new table to get started.")
            return

        # 1. High Level Dataframe
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
        st.subheader("Manage Orders")

        # 2. Detailed Cards (Accordion)
        for order in orders:
            t_label = getattr(order, "table_number", getattr(order, "table_id", "?"))
            label = (
                f"📋 Order #{order.id} | Table {t_label} | ${order.total_value:,.2f}"
            )

            with st.expander(label, expanded=False):
                # A. Order Details Table (Formerly in components/cards.py)
                self._render_order_items_table(order)
                st.divider()

                # B. Action Tabs
                tab_add, tab_rem, tab_pay = st.tabs(
                    ["Add Item", "Remove Item", "Pay & Close"]
                )

                with tab_add:
                    self._render_add_item_form(order.id)

                with tab_rem:
                    self._render_remove_item_form(order)

                with tab_pay:
                    st.caption("Review the total and proceed to payment.")
                    if st.button(
                        "💰 Pay & Close Order",
                        key=f"btn_close_{order.id}",
                        type="primary",
                    ):
                        if self.vm.close_order(order.id):
                            st.success(f"Order #{order.id} closed!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(self.vm.last_error)

    def _render_order_items_table(self, order):
        """Renders the read-only items table."""
        if not order.items:
            st.info("No items ordered yet.")
            return

        df_items = pd.DataFrame([item.model_dump() for item in order.items])

        # Calculate Subtotal if missing
        if "total_price" in df_items.columns and "subtotal" not in df_items.columns:
            df_items["subtotal"] = df_items["total_price"]

        cols = ["dish_name", "quantity", "unit_price", "subtotal"]
        display_cols = [c for c in cols if c in df_items.columns]

        st.dataframe(
            df_items[display_cols],
            width="stretch",
            hide_index=True,
            column_config={
                "unit_price": st.column_config.NumberColumn(format="$%.2f"),
                "subtotal": st.column_config.NumberColumn(format="$%.2f"),
            },
        )

    def _render_add_item_form(self, order_id: int):
        """Formerly in components/forms.py"""
        with st.form(key=f"add_item_{order_id}"):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                dish_id = st.number_input(
                    "Dish ID", min_value=1, step=1, key=f"d_{order_id}"
                )
            with c2:
                qty = st.number_input(
                    "Qty", min_value=1, step=1, value=1, key=f"q_{order_id}"
                )
            with c3:
                st.write("")  # Spacer
                submit = st.form_submit_button("Add")

            if submit:
                if self.vm.add_item_to_order(order_id, dish_id, qty):
                    st.toast(f"✅ Item added to Order #{order_id}")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(self.vm.last_error)

    def _render_remove_item_form(self, order):
        if not order.items:
            st.info("No items to remove.")
            return

        items_map = {
            item.id: f"{item.dish_name} (x{item.quantity})" for item in order.items
        }

        c1, c2 = st.columns([3, 1])
        with c1:
            selected_item_id = st.selectbox(
                "Select Item",
                options=items_map.keys(),
                format_func=lambda x: items_map[x],
                key=f"del_sel_{order.id}",
                label_visibility="collapsed",
            )
        with c2:
            if st.button("🗑️ Remove", key=f"btn_del_{order.id}"):
                if self.vm.remove_item_from_order(order.id, selected_item_id):
                    st.toast("Item removed.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(self.vm.last_error)

    def _render_create_order_tab(self):
        st.subheader("Open New Table")

        # Fetch options dynamically
        options = self.vm.get_new_order_options()

        if self.vm.last_error:
            st.error(self.vm.last_error)

        with st.form("new_order_form"):
            st.write("Select details to open a new tab:")
            c1, c2 = st.columns(2)
            with c1:
                c_id = st.selectbox(
                    "Select Customer",
                    options=options.customers.keys(),
                    format_func=lambda x: options.customers.get(x, "Unknown"),
                )
                w_id = st.selectbox(
                    "Assign Waiter",
                    options=options.waiters.keys(),
                    format_func=lambda x: options.waiters.get(x, "Unknown"),
                )

            with c2:
                if not options.tables:
                    st.warning("No free tables available.")
                    table_id = None
                else:
                    table_id = st.selectbox(
                        "Select Table",
                        options=options.tables.keys(),
                        format_func=lambda x: options.tables.get(x, "Unknown"),
                    )

                customer_count = st.number_input(
                    "Number of Guests", min_value=1, step=1, value=2
                )

            st.markdown("---")

            if table_id:
                warning = self.vm.check_table_capacity(table_id, customer_count)
                if warning:
                    st.warning(warning)

            disabled = table_id is None
            submitted = st.form_submit_button(
                "Open Table", width="stretch", disabled=disabled
            )

            if submitted:
                if not c_id or not table_id or not w_id:
                    st.error("Please select all fields.")
                else:
                    success = self.vm.create_order(c_id, table_id, w_id, customer_count)
                    if success:
                        st.success("✅ Table Opened Successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(self.vm.last_error)