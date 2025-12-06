import streamlit as st
import pandas as pd
import time
from services.order import OrderService
from services.customers import CustomerService
from components.cards import render_order_card
from components.forms import render_open_order_form
from utils.exceptions import AppError

order_service = OrderService()
customer_service = CustomerService()

st.set_page_config(page_title="Orders", page_icon="📝", layout="wide")
st.header("📝 Order Management")

tab_view, tab_create = st.tabs(["Active Orders", "Open New Table"])

def handle_add_item(order_id: int, dish_id: int, qty: int):
    """Controller function to handle Adding Items."""
    try:
        order_service.add_item(order_id, {"dish_id": dish_id, "quantity": qty})
        st.toast(f"✅ Item added to Order #{order_id}!")
        time.sleep(0.5)
        st.rerun()
    except AppError as e:
        st.error(f"Failed to add item: {e}")


with tab_view:
    try:
        orders_data = order_service.list_orders()

        if not orders_data:
            st.info("No active orders found. Go to 'Open New Table' to start.")
        else:
            df_orders = pd.DataFrame(orders_data)
            st.dataframe(
                df_orders[["id", "customer_name", "table_number", "total_value"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn(format="$%.2f")
                },
            )
            st.markdown("---")
            st.subheader("Order Actions")
            for order_summary in orders_data:
                render_order_card(order_summary, on_add_item=handle_add_item)

    except AppError as e:
        st.error(f"Error loading orders: {e}")

with tab_create:
    st.subheader("Open New Table")
    try:
        customers = customer_service.get_customers()
        c_options = {c["id"]: c["name"] for c in customers}
        submission_data = render_open_order_form(c_options)
        if submission_data:
            try:
                order_service.create_order(submission_data)
                st.success(
                    f"✅ Table {submission_data['table_id']} Opened Successfully!"
                )
                time.sleep(1)
                st.rerun()
            except AppError as e:
                st.error(f"Could not create order: {e}")

    except AppError as e:
        st.error(f"Could not load required data: {e}")