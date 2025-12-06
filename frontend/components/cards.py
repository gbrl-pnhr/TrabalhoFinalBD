import streamlit as st
import pandas as pd
from datetime import datetime
from schemas import OrderResponse


def render_order_details(order: OrderResponse):
    """
    Renders the details of an order (Items Table) using the Pydantic model.
    """
    items = order.items
    if items:
        df_items = pd.DataFrame([item.model_dump() for item in items])
        cols = ["dish_name", "quantity", "unit_price", "subtotal"]
        display_cols = [c for c in cols if c in df_items.columns]
        st.dataframe(
            df_items[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "unit_price": st.column_config.NumberColumn(format="$%.2f"),
                "subtotal": st.column_config.NumberColumn(format="$%.2f"),
            },
        )
    else:
        st.info("No items ordered yet.")


def render_kitchen_ticket(order: OrderResponse):
    """
    Renders a large, high-contrast ticket for the Kitchen Display System (KDS).
    """
    # Calculate time delta if created_at is available (assuming ISO format string)
    time_label = "Just Now"
    if hasattr(order, "created_at") and order.created_at:
        try:
            # Simple parsing - adjust based on actual backend format
            created_dt = datetime.fromisoformat(str(order.created_at))
            delta = datetime.now() - created_dt
            minutes = int(delta.total_seconds() / 60)
            time_label = f"{minutes} min ago"
        except Exception:
            pass

    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### 🍽️ Table {order.table_id}")
            st.caption(f"Order #{order.id} • Waiter ID: {order.waiter_id}")
        with c2:
            st.markdown(f"**{time_label}**")
            st.markdown("🔴 PREP")

        st.divider()

        if not order.items:
            st.warning("Empty Ticket")
        else:
            for item in order.items:
                st.markdown(f"#### **{item.quantity}x** {item.dish_name}")
                st.caption(f"{item.observacao}")