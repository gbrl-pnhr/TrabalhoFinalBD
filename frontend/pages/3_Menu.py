import streamlit as st
import pandas as pd
from services.menu import MenuService
from components.forms import render_create_dish_form
from utils.exceptions import AppError
from schemas import DishCreate

menu_service = MenuService()

st.set_page_config(page_title="Menu", page_icon="🍴", layout="wide")
st.header("🍴 Menu Management")

tab_list, tab_create = st.tabs(["Menu List", "Create Dish"])


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
            col1, _ = st.columns([1, 2])
            with col1:
                search_term = st.text_input("🔍 Search Dish:", "").lower()
            if search_term and not df_dishes.empty:
                mask = df_dishes["name"].str.lower().str.contains(search_term)
                df_dishes = df_dishes[mask]
            st.dataframe(
                df_dishes,
                use_container_width=True,
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
                category=new_dish_data["category"]
            )
            menu_service.create_dish(dish_payload)
            st.success(f"✅ Dish '{dish_payload.name}' created successfully!")
            st.cache_data.clear()
            st.rerun()
        except AppError as e:
            st.error(f"Failed to create dish: {e}")
        except ValueError as e:
            st.error(f"Validation Error: {e}")