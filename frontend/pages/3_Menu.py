import streamlit as st
from services.menu import fetch_dishes, create_dish

st.header("🍴 Menu Management")

tab1, tab2 = st.tabs(["List & Search", "Create New"])

with tab1:
    termo = st.text_input("Search Dish:", "")
    df_dishes = fetch_dishes()
    if not df_dishes.empty:
        if termo:
            df_dishes = df_dishes[df_dishes["name"].str.contains(termo, case=False)]
        st.dataframe(df_dishes, use_container_width=True)
    else:
        st.info("No dishes found.")

with tab2:
    with st.form("create_dish_form"):
        name = st.text_input("Dish Name")
        price = st.number_input("Price", min_value=0.01)
        category = st.text_input("Category")

        if st.form_submit_button("Create"):
            # OLD: criar_prato(...)
            # NEW:
            create_dish(name, price, category)
            st.success("Dish Created!")
            st.rerun()
