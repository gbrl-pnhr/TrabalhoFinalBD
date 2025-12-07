import streamlit as st
import pandas as pd
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
        st.header("📝 Order Management")

        self._handle_flash_messages()

        self.vm.load_active_orders()
        if self.vm.last_error:
            st.error(f"Error loading orders: {self.vm.last_error}")

        tab_list, tab_create = st.tabs(["Active Orders", "Open New Table"])

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
                    "text": "All fields are required.",
                }
                return

            if self.vm.create_order(c_id, t_id, w_id, count):
                st.session_state["flash_msg"] = {
                    "type": "success",
                    "text": "Table opened successfully!",
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
            st.toast(f"✅ Item added to Order #{order_id}")
        else:
            st.toast(f"❌ {self.vm.last_error}")

    def _handle_remove_item(self, order_id: int):
        sel_key = f"rem_item_sel_{order_id}"
        item_id = st.session_state.get(sel_key)

        if not item_id:
            st.toast("⚠️ No item selected.")
            return

        if self.vm.remove_item_from_order(order_id, item_id):
            st.toast("✅ Item removed.")
        else:
            st.toast(f"❌ {self.vm.last_error}")

    def _handle_close_order(self, order_id: int):
        if self.vm.close_order(order_id):
            st.session_state["flash_msg"] = {
                "type": "success",
                "text": f"Order #{order_id} closed & paid.",
            }
            st.rerun()
        else:
            st.toast(f"❌ {self.vm.last_error}")


    def _render_active_orders_tab(self):
        orders = self.vm.active_orders
        if not orders:
            st.info("No active orders found. Open a new table to get started.")
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
        st.subheader("Manage Orders")

        for order in orders:
            self._render_order_card_fragment(order.id)

    @st.fragment
    def _render_order_card_fragment(self, order_id: int):
        """
        Renders a single order card.
        Decorated with @st.fragment to enable granular re-rendering.
        When a user interacts with widgets inside this function, only this function re-runs.
        """

        order = self.vm.get_order_by_id(order_id)

        if not order or str(order.status).lower() in ["closed", "paid", "completed"]:
            return

        t_label = getattr(order, "table_number", getattr(order, "table_id", "?"))
        label = f"📋 Order #{order.id} | Table {t_label} | ${order.total_value:,.2f}"

        with st.expander(label, expanded=False):
            self._render_order_items_table(order)
            st.divider()

            tab_add, tab_rem, tab_pay = st.tabs(
                ["Add Item", "Remove Item", "Pay & Close"]
            )

            with tab_add:
                self._render_add_item_form(order.id)

            with tab_rem:
                self._render_remove_item_form(order)

            with tab_pay:
                st.caption("Review the total and proceed to payment.")
                st.button(
                    "💰 Pay & Close Order",
                    key=f"btn_close_{order.id}",
                    type="primary",
                    on_click=self._handle_close_order,
                    args=(order.id,),
                )

    def _render_order_items_table(self, order):
        if not order.items:
            st.info("No items ordered yet.")
            return

        df_items = pd.DataFrame([item.model_dump() for item in order.items])
        if "total_price" in df_items.columns:
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
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.number_input(
                "Dish ID", min_value=1, step=1, key=f"add_dish_id_{order_id}"
            )
        with c2:
            st.number_input(
                "Qty", min_value=1, step=1, value=1, key=f"add_qty_{order_id}"
            )
        with c3:
            st.write("")
            st.button(
                "Add",
                key=f"btn_add_{order_id}",
                on_click=self._handle_add_item,
                args=(order_id,)
            )

    def _render_remove_item_form(self, order):
        if not order.items:
            st.info("No items to remove.")
            return

        items_map = {
            item.id: f"{item.dish_name} (x{item.quantity})" for item in order.items
        }

        c1, c2 = st.columns([3, 1])
        with c1:
            st.selectbox(
                "Select Item",
                options=items_map.keys(),
                format_func=lambda x: items_map[x],
                key=f"rem_item_sel_{order.id}",
                label_visibility="collapsed",
            )
        with c2:
            st.button(
                "🗑️ Remove",
                key=f"btn_del_{order.id}",
                on_click=self._handle_remove_item,
                args=(order.id,),
            )

    def _render_create_order_tab(self):
        st.subheader("Open New Table")

        options = self.vm.get_new_order_options()
        if self.vm.last_error:
            st.error(self.vm.last_error)

        with st.form("new_order_form"):
            st.write("Select details to open a new tab:")
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox(
                    "Select Customer",
                    options=options.customers.keys(),
                    format_func=lambda x: options.customers.get(x, "Unknown"),
                    key="new_order_customer",
                )
                st.selectbox(
                    "Assign Waiter",
                    options=options.waiters.keys(),
                    format_func=lambda x: options.waiters.get(x, "Unknown"),
                    key="new_order_waiter",
                )

            with c2:
                if not options.tables:
                    st.warning("No free tables available.")
                    st.selectbox(
                        "Select Table", options=[], disabled=True, key="new_order_table"
                    )
                else:
                    st.selectbox(
                        "Select Table",
                        options=options.tables.keys(),
                        format_func=lambda x: options.tables.get(x, "Unknown"),
                        key="new_order_table",
                    )

                st.number_input(
                    "Number of Guests",
                    min_value=1,
                    step=1,
                    value=2,
                    key="new_order_count",
                )

            st.markdown("---")
            st.form_submit_button(
                "Open Table",
                width="stretch",
                on_click=self._handle_create_order,
                disabled=not options.tables
            )