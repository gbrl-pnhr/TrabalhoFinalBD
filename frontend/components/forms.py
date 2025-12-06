import streamlit as st
from typing import Dict, Any, Optional


def render_add_item_form(
    order_id: int, key_prefix: str = "add_item"
) -> Optional[Dict[str, int]]:
    """
    Renders a small form to add an item to an order.
    Returns a dictionary with {dish_id, quantity} if submitted, else None.
    """
    with st.form(key=f"{key_prefix}_{order_id}"):
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
            return {"dish_id": dish_id, "quantity": qty}
    return None


def render_create_dish_form() -> Optional[Dict[str, Any]]:
    """
    Renders the form to create a new menu dish.
    Returns dict {name, price, category} if submitted.
    """
    with st.form("create_dish_form"):
        st.subheader("New Dish Details")
        name = st.text_input("Dish Name")
        c1, c2 = st.columns(2)
        with c1:
            price = st.number_input(
                "Price ($)", min_value=0.01, step=0.50, format="%.2f"
            )
        with c2:
            category = st.selectbox(
                "Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Side"]
            )

        if st.form_submit_button("Create Dish", use_container_width=True):
            if not name:
                st.error("Dish name is required.")
                return None
            return {"name": name, "price": price, "category": category}
    return None


def render_open_order_form(
    customer_options: Dict[int, str],
) -> Optional[Dict[str, Any]]:
    """
    Renders the form to open a new table/order.
    Args:
        customer_options: Dict mapping ID -> Name
    Returns:
        Dict payload for order creation if submitted.
    """
    with st.form("new_order_form"):
        c1, c2 = st.columns(2)
        with c1:
            c_id = st.selectbox(
                "Select Customer",
                options=customer_options.keys(),
                format_func=lambda x: customer_options.get(x, "Unknown"),
            )
        with c2:
            table_id = st.number_input("Table Number", min_value=1, step=1)
        waiter_id = st.number_input("Waiter ID", min_value=1, step=1)
        customer_count = st.number_input("Waiter ID", min_value=1, step=1)
        st.markdown("---")
        if st.form_submit_button("Open Table", use_container_width=True):
            return {
                "customer_id": c_id,
                "table_id": table_id,
                "waiter_id": waiter_id,
                "customer_count": customer_count,
            }
    return None