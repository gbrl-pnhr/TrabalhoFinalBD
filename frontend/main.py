import streamlit as st

st.set_page_config(layout="wide", page_title="Restaurant Manager")

st.title("🍽️ Restaurant Management System")

st.markdown("""
Selecione a module from the sidebar to begin managing:
- **Orders:** Manage tables and current orders.
- **Menu:** Update prices and add dishes.
- **Customers:** View clients and reviews.
- **Staff:** Manage waiters and cooks.
""")