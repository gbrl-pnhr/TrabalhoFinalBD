import streamlit as st
from typing import Dict, Any, Optional, List


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
            st.write("")
            submit = st.form_submit_button("Add")

        if submit:
            return {"dish_id": dish_id, "quantity": qty}
    return None


def render_create_dish_form(
    existing_categories: List[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Renders the form to create a new menu dish.
    Allows selecting existing category or typing a new one.
    Returns dict {name, price, category} if submitted.
    """
    if existing_categories is None:
        existing_categories = []
    NEW_CAT_OPTION = "➕ Create New Category..."
    options = existing_categories + [NEW_CAT_OPTION]
    st.subheader("New Dish Details")
    c_cat1, c_cat2 = st.columns(2)
    with c_cat1:
        selected_cat = st.selectbox("Category", options)
    final_category = selected_cat
    if selected_cat == NEW_CAT_OPTION:
        with c_cat2:
            final_category = st.text_input(
                "Enter New Category Name", placeholder="e.g. Vegan Specials"
            )
    with st.form("create_dish_form"):
        name = st.text_input("Dish Name")
        c_price, _ = st.columns(2)
        with c_price:
            price = st.number_input(
                "Price ($)", min_value=0.01, step=0.50, format="%.2f"
            )
        if st.form_submit_button("Create Dish", width="stretch"):
            if not name:
                st.error("Dish name is required.")
                return None
            if (
                not final_category
                or final_category == NEW_CAT_OPTION
                or final_category.strip() == ""
            ):
                st.error("Please provide a valid category.")
                return None

            return {"name": name, "price": price, "category": final_category}
    return None


def render_open_order_form(
    customer_options: Dict[int, str],
    table_options: Dict[int, str],
    waiter_options: Dict[int, str],
) -> Optional[Dict[str, Any]]:
    """
    Renders the form to open a new table/order using Dropdowns.
    Args:
        customer_options: Dict mapping Customer ID -> Name
        table_options: Dict mapping Table ID -> Label (e.g. "Table 1 (4 seats)")
        waiter_options: Dict mapping Waiter ID -> Name
    Returns:
        Dict payload for order creation if submitted.
    """
    with st.form("new_order_form"):
        st.write("Select details to open a new tab:")
        c1, c2 = st.columns(2)
        with c1:
            c_id = st.selectbox(
                "Select Customer",
                options=customer_options.keys(),
                format_func=lambda x: customer_options.get(x, "Unknown"),
                help="Who is paying the bill?",
            )
            w_id = st.selectbox(
                "Assign Waiter",
                options=waiter_options.keys(),
                format_func=lambda x: waiter_options.get(x, "Unknown"),
            )

        with c2:
            if not table_options:
                st.warning("No tables available/free!")
                table_id = None
            else:
                table_id = st.selectbox(
                    "Select Table",
                    options=table_options.keys(),
                    format_func=lambda x: table_options.get(x, "Unknown"),
                )
            customer_count = st.number_input(
                "Number of Guests", min_value=1, step=1, value=2
            )

        st.markdown("---")
        disabled = table_id is None
        if st.form_submit_button("Open Table", width="stretch", disabled=disabled):
            if not c_id or not table_id or not w_id:
                st.error("Please select all fields.")
                return None

            return {
                "customer_id": c_id,
                "table_id": table_id,
                "waiter_id": w_id,
                "customer_count": customer_count,
            }
    return None