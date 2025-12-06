import streamlit as st
import pandas as pd
import time
from services.order import OrderService
from services.customers import CustomerService
from services.tables import TableService
from services.staff import StaffService
from components.cards import render_order_details
from components.forms import render_add_item_form, render_open_order_form
from utils.exceptions import AppError
from schemas import OrderCreate, OrderItemCreate

order_service = OrderService()
customer_service = CustomerService()
table_service = TableService()
staff_service = StaffService()

st.set_page_config(page_title="Orders", page_icon="📝", layout="wide")
st.header("📝 Order Management")

tab_view, tab_create = st.tabs(["Active Orders", "Open New Table"])


def handle_add_item(order_id: int, dish_id: int, qty: int):
    try:
        item_payload = OrderItemCreate(dish_id=dish_id, quantity=qty)
        order_service.add_item(order_id, item_payload)
        st.toast(f"✅ Item added to Order #{order_id}!")
        time.sleep(0.5)
        st.rerun()
    except AppError as e:
        st.error(f"Failed to add item: {e}")
    except ValueError as e:
        st.error(f"Validation Error: {e}")


def handle_remove_item(order_id: int, item_id: int):
    try:
        order_service.remove_item(order_id, item_id)
        st.toast(f"🗑️ Item removed from Order #{order_id}")
        time.sleep(0.5)
        st.rerun()
    except AppError as e:
        st.error(f"Failed to remove item: {e}")


with tab_view:
    try:
        orders_data = order_service.list_orders()
        active_orders = [
            o
            for o in orders_data
            if str(o.status).lower() not in ["closed", "paid", "completed"]
        ]
        if not active_orders:
            st.info("No active orders found. Go to 'Open New Table' to start.")
        else:
            df_orders = pd.DataFrame([o.model_dump() for o in active_orders])
            cols = ["id", "customer_name", "table_number", "total_value", "status"]
            display_cols = [c for c in cols if c in df_orders.columns]
            st.dataframe(
                df_orders[display_cols],
                width='stretch',
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn(format="$%.2f")
                },
            )
            st.markdown("---")
            st.subheader("Manage Active Orders")
            for order in active_orders:
                label = f"📋 Order #{order.id} | Table {order.table_id} | ${order.total_value:,.2f}"
                with st.expander(label, expanded=False):
                    render_order_details(order)
                    st.divider()
                    tab_add, tab_rem, tab_pay = st.tabs(
                        ["Add Item", "Remove Item", "Pay & Close"]
                    )
                    with tab_add:
                        form_data = render_add_item_form(order.id)
                        if form_data:
                            handle_add_item(
                                order.id,
                                form_data["dish_id"],
                                form_data["quantity"],
                            )
                    with tab_rem:
                        if order.items:
                            items_map = {
                                item.id: f"{item.dish_name} (x{item.quantity})"
                                for item in order.items
                            }
                            selected_item_id = st.selectbox(
                                "Select Item to Remove",
                                options=items_map.keys(),
                                format_func=lambda x: items_map[x],
                                key=f"del_sel_{order.id}",
                            )
                            if st.button(
                                "🗑️ Remove Selected Item", key=f"btn_del_{order.id}"
                            ):
                                handle_remove_item(order.id, selected_item_id)
                        else:
                            st.info("No items to remove.")
                    with tab_pay:
                        st.write("Ready to close?")
                        if st.button(
                            "💰 Pay & Close Order",
                            key=f"btn_close_{order.id}",
                            type="primary",
                        ):
                            try:
                                order_service.close_order(order.id)
                                st.success(f"Order #{order.id} closed!")
                                time.sleep(1)
                                st.rerun()
                            except AppError as e:
                                st.error(f"Failed to close: {e}")

    except AppError as e:
        st.error(f"Error loading orders: {e}")

with tab_create:
    st.subheader("Open New Table")
    try:
        customers = customer_service.get_customers()
        tables = table_service.get_tables()
        waiters = staff_service.get_waiters()
        c_options = {c.id: c.name for c in customers}
        t_options = {
            t.id: f"Table {t.number} ({t.capacity} Seats) - {t.location}"
            for t in tables
            if not t.is_occupied
        }
        w_options = {w.id: f"{w.name}" for w in waiters}
        submission_data = render_open_order_form(c_options, t_options, w_options)
        if submission_data:
            try:
                new_order = OrderCreate(
                    customer_id=submission_data["customer_id"],
                    table_id=submission_data["table_id"],
                    waiter_id=submission_data["waiter_id"],
                    customer_count=submission_data["customer_count"],
                )
                order_service.create_order(new_order)
                st.success(f"✅ Table Opened Successfully!")
                time.sleep(1)
                st.rerun()
            except AppError as e:
                st.error(f"Could not create order: {e}")
            except ValueError as e:
                st.error(f"Input Validation Error: {e}")

    except AppError as e:
        st.error(f"Could not load required data. Is the backend online? Error: {e}")