import sys
from pathlib import Path
import streamlit as st
ROOT_PATH = Path(__file__).parent
sys.path.append(str(ROOT_PATH))
from components.sidebar import render_global_sidebar

st.set_page_config(
    page_title="Restaurant Manager",
    page_icon="🍽️",
    layout="wide"
)

pages_structure = {
    "Analytics": [
        st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊", default=True),
    ],
    "Operations": [
        st.Page("pages/2_Orders.py", title="Active Orders", icon="📝"),
        st.Page("pages/8_Kitchen.py", title="Kitchen Display", icon="🍳"),
    ],
    "Management": [
        st.Page("pages/3_Menu.py", title="Menu Management", icon="🍴"),
        st.Page("pages/6_Tables.py", title="Table Layout", icon="🪑"),
        st.Page("pages/4_Staff.py", title="Staff", icon="👨‍🍳"),
        st.Page("pages/5_Customers.py", title="Customers", icon="👥"),
        st.Page("pages/7_Reviews.py", title="Reviews", icon="⭐"),
    ]
}

render_global_sidebar(pages_structure)

pg = st.navigation(pages_structure, position="hidden")
pg.run()