import streamlit as st
import pandas as pd
import time

from apps.api.modules import DishCreate, DishUpdate
from apps.ui.services.menu import MenuService
from apps.ui.components.forms import render_create_dish_form
from apps.ui.utils.exceptions import AppError

menu_service = MenuService()

st.header("🍴 Menu Management")

tab_list, tab_create, tab_manage = st.tabs(
    ["Menu List", "Create Dish", "Manage (Edit/Delete)"]
)

@st.cache_data(ttl=300)
def get_cached_menu():
    return menu_service.get_dishes()

with tab_list:
    try:
        dishes_data = get_cached_menu()
        if not dishes_data:
            st.info("No dishes found in the menu.")
        else:
            df_dishes = pd.DataFrame([d.model_dump() for d in dishes_data])
            st.dataframe(
                df_dishes,
                width='stretch',
                hide_index=True,
                column_config={"price": st.column_config.NumberColumn(format="$%.2f")},
            )
            if st.button("Refresh List"):
                st.cache_data.clear()
                st.rerun()
    except AppError as e:
        st.error(f"Error loading menu: {e}")

with tab_create:
    new_dish_data = render_create_dish_form()
    if new_dish_data:
        try:
            dish_payload = DishCreate(
                name=new_dish_data["name"],
                price=new_dish_data["price"],
                category=new_dish_data["category"],
            )
            menu_service.create_dish(dish_payload)
            st.success(f"✅ Dish '{dish_payload.name}' created successfully!")
            st.cache_data.clear()
            st.rerun()
        except AppError as e:
            st.error(f"Failed to create dish: {e}")
        except ValueError as e:
            st.error(f"Validation Error: {e}")

with tab_manage:
    st.subheader("Edit or Remove Dishes")
    try:
        dishes = get_cached_menu()
        if dishes:
            dish_map = {d.id: f"{d.name} (${d.price})" for d in dishes}
            selected_id = st.selectbox(
                "Select Dish to Edit",
                options=dish_map.keys(),
                format_func=lambda x: dish_map[x],
            )
            selected_dish = next((d for d in dishes if d.id == selected_id), None)
            if selected_dish:
                with st.form(key="edit_dish_form"):
                    st.write(f"Editing: **{selected_dish.name}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_price = st.number_input(
                            "New Price ($)", value=float(selected_dish.price), step=0.5
                        )
                    with col2:
                        new_name = st.text_input("New Name", value=selected_dish.name)

                    update_btn = st.form_submit_button("💾 Update Dish Details")
                st.write("")
                delete_btn = st.button("🗑️ Permanently Delete Dish", type="primary")
                if update_btn:
                    try:
                        update_payload = DishUpdate(name=new_name, price=new_price)
                        menu_service.update_dish(selected_id, update_payload)
                        st.success("✅ Dish updated!")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    except AppError as e:
                        st.error(f"Update failed: {e}")
                if delete_btn:
                    try:
                        menu_service.delete_dish(selected_id)
                        st.warning("🗑️ Dish deleted.")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    except AppError as e:
                        st.error(f"Delete failed: {e}")

    except AppError as e:
        st.error(f"Could not load menu: {e}")