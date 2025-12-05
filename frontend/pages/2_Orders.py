import streamlit as st
import pandas as pd

from services.orders import fetch_orders_with_details, create_order, add_item_to_order
from services.customers import fetch_customers

st.header("📝 Order Management")

tab_view, tab_create = st.tabs(["Active Orders", "New Order"])

# --- VIEW ORDERS TAB ---
with tab_view:
    # OLD: df_pedidos = fetch_all_pedidos_completos()
    # NEW: API Call
    orders_data = fetch_orders_with_details()

    if orders_data:
        # Convert JSON list to DataFrame for display
        df_orders = pd.DataFrame(orders_data)

        st.dataframe(
            df_orders[["id", "customer_name", "table_number", "total_value"]],
            use_container_width=True,
        )

        st.markdown("---")
        st.subheader("Order Details")

        # Logic to expand details
        for order in orders_data:
            label = f"📋 Order #{order['id']} - {order['customer_name']}"
            with st.expander(label):
                # The items should be nested in the order JSON response now
                items = order.get("items", [])
                if items:
                    df_items = pd.DataFrame(items)
                    st.dataframe(df_items, use_container_width=True)
                else:
                    st.info("No items in this order.")

                # Add Item Form (Inside the expander - nice UI touch)
                with st.form(f"add_item_{order['id']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        # You would fetch dishes from API here
                        dish_id = st.number_input(
                            "Dish ID", step=1, key=f"d_{order['id']}"
                        )
                    with col2:
                        qty = st.number_input(
                            "Qty", min_value=1, key=f"q_{order['id']}"
                        )

                    if st.form_submit_button("Add Item"):
                        add_item_to_order(order["id"], dish_id, qty)
                        st.rerun()

# --- CREATE ORDER TAB ---
with tab_create:
    st.subheader("Open New Table")

    # Fetch lists for dropdowns
    customers = fetch_customers()  # Returns list of dicts [{'id': 1, 'name': 'Bob'}]

    with st.form("new_order_form"):
        # Dropdown Logic
        c_options = {c["id"]: c["name"] for c in customers}
        c_id = st.selectbox(
            "Customer", options=c_options.keys(), format_func=lambda x: c_options[x]
        )

        # (Assuming you do same for Tables and Waiters...)

        if st.form_submit_button("Open Order"):
            create_order(customer_id=c_id, table_id=1, waiter_id=1)  # Example
            st.success("Order Opened!")
