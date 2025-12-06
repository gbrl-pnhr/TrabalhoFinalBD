import streamlit as st
import pandas as pd
import time
from services.order import OrderService
from services.customers import CustomerService
from components.cards import render_order_details
from components.forms import render_add_item_form, render_open_order_form
from utils.exceptions import AppError
from schemas import OrderCreate, OrderItemCreate

order_service = OrderService()
customer_service = CustomerService()

st.set_page_config(page_title="Orders", page_icon="📝", layout="wide")
st.header("📝 Order Management")

tab_view, tab_create = st.tabs(["Active Orders", "Open New Table"])


def handle_add_item(order_id: int, dish_id: int, qty: int):
    """Controller function for adding items."""
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


with tab_view:
    try:
        orders_data = order_service.list_orders()

        if not orders_data:
            st.info("No active orders found. Go to 'Open New Table' to start.")
        else:
            df_orders = pd.DataFrame([o.model_dump() for o in orders_data])
            cols = ["id", "customer_name", "table_number", "total_value"]
            display_cols = [c for c in cols if c in df_orders.columns]
            st.dataframe(
                df_orders[display_cols],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn(format="$%.2f")
                },
            )
            st.markdown("---")
            st.subheader("Order Actions")
            for order in orders_data:
                label = f"📋 Order #{order.id} | {order.customer_name or 'Unknown'} | ${order.total_value:,.2f} | Status: {order.status}"
                is_closed = str(order.status).lower() in ["closed", "completed", "paid"]
                with st.expander(label, expanded=False):
                    render_order_details(order)
                    st.divider()
                    if not is_closed:
                        col_act1, col_act2 = st.columns([3, 1])
                        with col_act1:
                            st.caption("Add Item to Order")
                            form_data = render_add_item_form(order.id)
                            if form_data:
                                handle_add_item(
                                    order.id,
                                    form_data["dish_id"],
                                    form_data["quantity"],
                                )
                        with col_act2:
                            st.write("")
                            st.write("")
                            st.write("")
                            if st.button(
                                "💰 Pay & Close",
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
                    else:
                        st.info("✅ This order is closed and paid.")
    except AppError as e:
        st.error(f"Error loading orders: {e}")

with tab_create:
    st.subheader("Open New Table")
    try:
        customers = customer_service.get_customers()
        c_options = {c.id: c.name for c in customers}
        submission_data = render_open_order_form(c_options)
        if submission_data:
            try:
                new_order = OrderCreate(
                    customer_id=submission_data["customer_id"],
                    table_id=submission_data["table_id"],
                    waiter_id=submission_data["waiter_id"],
                    customer_count=submission_data["customer_count"],
                )
                order_service.create_order(new_order)
                st.success(f"✅ Table {new_order.table_id} Opened Successfully!")
                time.sleep(1)
                st.rerun()
            except AppError as e:
                st.error(f"Could not create order: {e}")
            except ValueError as e:
                st.error(f"Input Validation Error: {e}")

    except AppError as e:
        st.error(f"Could not load required data: {e}")