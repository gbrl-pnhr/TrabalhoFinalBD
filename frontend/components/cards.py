import streamlit as st
import pandas as pd
from typing import Dict, Any


def render_order_details(order: Dict[str, Any]):
    """
    Renders the details of an order (Items Table).
    """
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