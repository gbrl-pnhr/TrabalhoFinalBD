import streamlit as st
import pandas as pd
from typing import Dict, Any, Callable
from components.forms import render_add_item_form


def render_order_card(
    order: Dict[str, Any], on_add_item: Callable[[int, int, int], None]
):
    """
    Renders a detailed card for a single active order.
    Uses the decoupled form component for actions.
    """
    order_id = order.get("id")
    customer = order.get("customer_name", "Unknown")
    total = order.get("total_value", 0.0)

    label = f"📋 Order #{order_id} | {customer} | ${total:,.2f}"

    with st.expander(label, expanded=False):
        items = order.get("items", [])
        if items:
            df_items = pd.DataFrame(items)
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
        st.divider()
        st.caption("Add Item to Order")
        form_data = render_add_item_form(order_id)
        if form_data:
            on_add_item(order_id, form_data["dish_id"], form_data["quantity"])