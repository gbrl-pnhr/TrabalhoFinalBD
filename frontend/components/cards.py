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
        if "total_price" in df_items.columns and "subtotal" not in df_items.columns:
            df_items["subtotal"] = df_items["total_price"]
        display_cols = [c for c in cols if c in df_items.columns]
        st.dataframe(
            df_items[display_cols],
            width="stretch",
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