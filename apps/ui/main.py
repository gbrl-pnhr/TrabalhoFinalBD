import streamlit as st
from components.sidebar import render_global_sidebar
from concurrent.futures import ThreadPoolExecutor
from apps.ui.services.menu import MenuService
from apps.ui.services.tables import TableService

st.set_page_config(page_title="Gerenciador de Restaurante", page_icon="🍽️", layout="wide")

def warm_up_cache():
    """
    Prefetch small, globally used data in the background.
    """
    menu_service = MenuService()
    table_service = TableService()
    with ThreadPoolExecutor() as executor:
        executor.submit(menu_service.get_categories)
        executor.submit(table_service.get_tables)

warm_up_cache()

pages_structure = {
    "Analytics": [
        st.Page("pages/1_Dashboard.py", title="Painel Geral", icon="📊", default=True),
    ],
    "Operations": [
        st.Page("pages/2_Orders.py", title="Pedidos Ativos", icon="📝"),
        st.Page("pages/8_Kitchen.py", title="Cozinha", icon="🍳"),
    ],
    "Management": [
        st.Page("pages/3_Menu.py", title="Menus", icon="🍴"),
        st.Page("pages/6_Tables.py", title="Posição das Mesas", icon="🪑"),
        st.Page("pages/4_Staff.py", title="Funcionários", icon="👨‍🍳"),
        st.Page("pages/5_Customers.py", title="Clientes", icon="👥"),
        st.Page("pages/7_Reviews.py", title="Avalizações", icon="⭐"),
    ]
}

render_global_sidebar(pages_structure)

pg = st.navigation(pages_structure, position="hidden")
pg.run()