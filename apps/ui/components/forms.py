import streamlit as st
from typing import Dict, Any, Optional, List

def render_create_dish_form(
    existing_categories: List[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Renders the form to create a new menu dish.
    Used in pages/3_Menu.py
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