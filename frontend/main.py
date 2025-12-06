import streamlit as st

st.set_page_config(
    page_title="Restaurant Manager",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Restaurant Management System")
st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1000&q=80", use_container_width=True)

st.markdown("""
### Welcome to the Management Portal

Use the sidebar menu to navigate through the modules:

1.  **Dashboard**: View real-time analytics on revenue and staff.
2.  **Orders**: Manage active tables and open orders.
3.  **Menu**: Create and edit dishes.
4.  **Staff**: Manage waiters and chefs.

**System Status:**
- Frontend: ✅ Online
- Backend Connection: (Check Dashboard)
""")