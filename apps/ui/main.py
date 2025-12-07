import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from components.sidebar import render_global_sidebar

st.set_page_config(
    page_title="Gerenciador de Restaurante",
    page_icon="🍽️",
    layout="wide"
)

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