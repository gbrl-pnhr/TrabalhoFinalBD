import streamlit as st
import time
from services.order import OrderService
from components.cards import render_kitchen_ticket
from utils.exceptions import AppError

st.title("🍳 Kitchen Display System (KDS)")
order_service = OrderService()

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

REFRESH_INTERVAL = 30

def get_active_orders():
    """Fetch orders that are not closed."""
    try:
        orders = order_service.list_orders()
        active = [
            o
            for o in orders
            if str(o.status).lower() not in ["closed", "paid", "completed"]
            and o.items
        ]
        return active
    except AppError:
        return None

placeholder = st.empty()
refresher = st.empty()

with placeholder.container():
    orders = get_active_orders()
    if orders is None:
        st.error("🔌 Connection to Backend Lost")
    elif not orders:
        st.success("✅ All tickets cleared! Kitchen is quiet.")
    else:
        cols = st.columns(3)
        for i, order in enumerate(orders):
            col = cols[i % 3]
            with col:
                render_kitchen_ticket(order)

with refresher:
    st.markdown("---")
    c1, c2 = st.columns([6, 1])
    with c1:
        st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")
    with c2:
        if st.button("🔄 Refresh"):
            st.rerun()