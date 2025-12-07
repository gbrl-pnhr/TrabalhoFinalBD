import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from datetime import datetime
from apps.api.modules import OrderResponse


def render_kitchen_ticket(order: OrderResponse):
    """
    Renders a large, high-contrast ticket for the Kitchen Display System (KDS).
    Used in pages/8_Kitchen.py
    """
    time_label = "Just Now"
    if hasattr(order, "created_at") and order.created_at:
        try:
            if isinstance(order.created_at, datetime):
                created_dt = order.created_at
            else:
                created_dt = datetime.fromisoformat(str(order.created_at))

            delta = datetime.now() - created_dt
            minutes = int(delta.total_seconds() / 60)
            time_label = f"{minutes} min ago"
        except Exception:
            pass
    table_disp = getattr(order, "table_number", getattr(order, "table_id", "?"))
    waiter_disp = getattr(order, "waiter_name", getattr(order, "waiter_id", "?"))
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### 🍽️ Table {table_disp}")
            st.caption(f"Order #{order.id} • Waiter: {waiter_disp}")
        with c2:
            st.markdown(f"**{time_label}**")
            st.markdown("🔴 PREP")
        st.divider()
        if not order.items:
            st.warning("Empty Ticket")
        else:
            for item in order.items:
                st.markdown(f"#### **{item.quantity}x** {item.dish_name}")
                if item.notes:
                    st.caption(f"📝 {item.notes}")